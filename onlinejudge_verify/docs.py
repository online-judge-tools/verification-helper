# -*- coding: utf-8 -*-
import glob
import hashlib
import os
import pathlib
import re
import shlex
import shutil
import subprocess
# typing.OrderedDict is not recognized by mypy
from collections import OrderedDict
from typing import IO, Any, Dict, List, Tuple

import markdown
import pkg_resources

package = 'onlinejudge_verify.data'
assets_site_header_txt = pkg_resources.resource_string(package, 'assets/site-header.txt')
deployed_assets = [
    {
        'path': pathlib.Path('assets/css/copy-button.css'),
        'data': pkg_resources.resource_string(package, 'assets/css/copy-button.css'),
    },
    {
        'path': pathlib.Path('assets/js/copy-button.js'),
        'data': pkg_resources.resource_string(package, 'assets/js/copy-button.js'),
    },
    {
        'path': pathlib.Path('_config.yml'),
        'data': pkg_resources.resource_string(package, 'assets/_config.yml'),
    },
]


class FileParser:
    # ファイルパスをもらって、行ごとに分ける
    def __init__(self, file_path: pathlib.Path) -> None:
        if not file_path.exists():
            raise FileNotFoundError('{} does not exist'.format(file_path))
        with open(file_path, 'rb') as f:
            self.lines = [line.decode().strip() for line in f.readlines()]

    # タグをもらって、コンテンツの配列を出す
    def get_contents_by_tag(self, tag_name: str, l_pat: str = '', r_pat: str = '') -> List[str]:
        tag_name = re.escape(tag_name)
        l_pat, r_pat = re.escape(l_pat), re.escape(r_pat)

        reg1, reg2 = r'^.*' + tag_name, r'^.*' + tag_name
        if l_pat != '':
            reg1 += r'.*' + l_pat
            reg2 += r'.*' + l_pat
        reg1 += r'.*'
        reg2 += r'(.*)'
        if r_pat != '':
            reg1 += r_pat + r'.*'
            reg2 += r_pat + r'.*'
        reg1 += r'$'
        reg2 += r'$'

        matches = [line for line in self.lines if re.match(reg1, line)]
        results = [re.sub(reg2, r'\1', line).strip() for line in matches]
        return results

    def get_implicit_dependencies(self) -> List[str]:
        reg1 = r'^#include[ ]*".*".*$'
        matches = [line for line in self.lines if re.match(reg1, line)]
        reg2 = r'^#include[ ]*"(.*)".*$'
        results = [re.sub(reg2, r'\1', line).strip() for line in matches]
        return results


# 現状は C++ のみのサポートを考える
class CppFile:
    # file_path: 対象としている C++ ファイル (source_path 内にあるファイル) へのパス
    # source_path: 検索対象となっているディレクトリへのパス
    def __init__(self, file_path: pathlib.Path, source_path: pathlib.Path) -> None:
        self.file_path = file_path.resolve()
        self.source_path = source_path.resolve()
        self.parser = FileParser(file_path)

        # file 指定が空なら、source_path から見た file_path へのパスをタイトルにする
        title_list = self.parser.get_contents_by_tag(r'@file')
        if title_list == []:
            self.title = str(self.file_path.relative_to(self.source_path))
        else:
            # @title が複数あるなら最後を採用？？
            self.title = title_list[-1]

        self.brief = self.parser.get_contents_by_tag(r'@brief')
        self.brief.extend(self.parser.get_contents_by_tag(r'#define DESCRIPTION', r'"', r'"'))

        # category 指定が空なら、source_path から見た file_path が属するディレクトリ名をカテゴリにする
        category_list = self.parser.get_contents_by_tag(r'@category')
        category_list.extend(self.parser.get_contents_by_tag(r'#define CATEGORY', r'"', r'"'))
        if category_list == []:
            self.category = str(self.file_path.parent.relative_to(self.source_path))
        else:
            self.category = category_list[-1]

        # see で指定されるのは URL: パス修正は不要
        self.see = self.parser.get_contents_by_tag(r'@see')
        self.see.extend(self.parser.get_contents_by_tag(r'#define PROBLEM', r'"', r'"'))
        self.see.extend(self.parser.get_contents_by_tag(r'#define SEE', r'"', r'"'))

        # pathlib 型に直し、相対パスである場合は絶対パスに直す
        docs_list = self.parser.get_contents_by_tag(r'@docs')
        docs_list.extend(self.parser.get_contents_by_tag(r'#define DOCS', r'"', r'"'))
        self.docs = [pathlib.Path(path) for path in docs_list]
        self.docs = self.to_abspath(self.docs)

        # pathlib 型に直し、相対パスである場合は絶対パスに直す
        depends_list = self.parser.get_contents_by_tag(r'@depends')
        depends_list.extend(self.parser.get_implicit_dependencies())
        depends_list.extend(self.parser.get_contents_by_tag(r'#define REQUIRES', r'"', r'"'))
        depends_list.extend(self.parser.get_contents_by_tag(r'#define DEPENDS', r'"', r'"'))
        self.depends = [pathlib.Path(path) for path in depends_list]
        self.depends = self.to_abspath(self.depends)
        self.depends.sort()

        self.required = []  # type: List[pathlib.Path]
        self.is_verified = self.get_verification_status()

    def get_verification_status(self) -> bool:
        for compiler in ('g++', 'clang++'):
            timestamp_path = pathlib.Path('.verify-helper/timestamp') / hashlib.md5(compiler.encode() + b'/./' + str(self.file_path.relative_to(self.source_path)).encode()).hexdigest()
            if not timestamp_path.exists():
                return False
            code = r"""{} --std=c++17 -O2 -Wall -g -I . -MD -MF /dev/stdout -MM {} | sed '1s/[^:].*: // ; s/\\$//' | xargs -n 1 | xargs git log -1 --date=iso --pretty=%ad""".format(compiler, shlex.quote(str(self.file_path)))
            timestamp = subprocess.check_output(code, shell=True).decode()
            with open(str(timestamp_path), 'rb') as fh:
                if fh.read().decode() < timestamp:
                    return False
        return True

    # self.file_path からの相対パスを絶対パスに直す
    def to_abspath(self, item_list: List[pathlib.Path]) -> List[pathlib.Path]:
        result, file_dir = [], self.file_path.parent
        for item in item_list:
            # とりあえず連結して存在するなら相対パス扱い
            abspath_cand = file_dir / item
            if abspath_cand.exists():
                result.append(abspath_cand.resolve())
            else:
                result.append(item.resolve())
        return result

    def set_required(self, required_list: List[pathlib.Path]) -> None:
        self.required = required_list
        self.required.sort()


class MarkdownPage:
    def __init__(self) -> None:
        self.cpp_source_path = pathlib.Path()
        self.md_destination_path = pathlib.Path()
        self.destination = pathlib.Path()

    def get_mark(self, cond: bool) -> str:
        if cond:
            return ':heavy_check_mark:'
        else:
            return ':warning:'

    # file_path の markdown 生成先はどのような絶対パスになるべきか
    # prefix は [cpp_source_path までのパス] でなければならない
    # [markdown 生成先ディレクトリまでのパス] + [file_type] + [cpp_source_path より深いパス] を返す？
    def get_destination(self, file_path: pathlib.Path, file_type: str = '') -> pathlib.Path:
        try:
            file_path.relative_to(self.cpp_source_path)
        except ValueError:
            raise ValueError('{} does not have prefix {}\n'.format(str(file_path), str(self.cpp_source_path)))

        file_path = file_path.resolve()
        path_suf = file_path.relative_to(self.cpp_source_path)
        return (self.md_destination_path / file_type / path_suf).resolve()

    # ページ A からページ B (link_href) への相対パスを得る
    # 全部絶対パスで持っているので relpath するだけでいいはず
    def get_link(self, link_href: pathlib.Path) -> str:
        return os.path.relpath(str(link_href), str(self.destination.parent))

    def make_directory(self) -> None:
        dir_name = self.destination.parent
        dir_name.mkdir(parents=True, exist_ok=True)

    def include_js(self, file_object: IO, js_file_name: pathlib.Path) -> None:
        js_file_link = self.get_link(js_file_name)
        html = '<script type="text/javascript" src="{}"></script>\n'.format(js_file_link)
        file_object.write(html.encode())

    def include_css(self, file_object: IO, css_file_name: pathlib.Path) -> None:
        css_file_link = self.get_link(css_file_name)
        html = '<link rel="stylesheet" href="{}" />\n'.format(css_file_link)
        file_object.write(html.encode())

    def convert_to_html(self) -> None:
        md_destination = str(self.destination) + '.md'
        html_destination = str(self.destination) + '.html'
        data = markdown.markdownFromFile(input=md_destination, output=html_destination, encoding="utf-8", extensions=['fenced_code', 'tables'])


class MarkdownArticle(MarkdownPage):
    def __init__(self, file_class: CppFile, file_type: str, cpp_source_path: pathlib.Path, md_destination_path: pathlib.Path) -> None:
        self.file_class = file_class
        self.cpp_source_path = cpp_source_path.resolve()
        self.md_destination_path = md_destination_path.resolve()
        self.destination = self.get_destination(self.file_class.file_path, file_type)
        self.mark = self.get_mark(self.file_class.is_verified)

    # include (mathjax, js, css)
    def write_header(self, file_object: IO) -> None:
        file_object.write(assets_site_header_txt)
        self.include_js(file_object, self.md_destination_path / './assets/js/copy-button.js')
        self.include_css(file_object, self.md_destination_path / './assets/css/copy-button.css')
        file_object.write('\n\n'.encode())

    def write_title(self, file_object: IO, category: str, categorize: bool) -> None:
        file_object.write('# {} {}\n'.format(self.mark, self.file_class.title).encode())
        if categorize: file_object.write('* category: {}\n'.format(category).encode())
        file_object.write('\n\n'.encode())

    def write_contents(self, file_object: IO, path_to_title: 'OrderedDict[pathlib.Path, str]', path_to_verification: Dict[pathlib.Path, bool]) -> None:
        back_to_top_link = self.get_link(self.md_destination_path / 'index.html')

        # back to top
        file_object.write('[Back to top page]({})\n\n'.format(back_to_top_link).encode())

        # brief, see, docs (絶対パス)
        for brief in self.file_class.brief:
            file_object.write('* {}\n'.format(brief).encode())
        for see in self.file_class.see:
            file_object.write('* see: [{}]({})\n'.format(see, see).encode())
        for docs in self.file_class.docs:
            with open(docs, 'rb') as f:
                file_object.write(f.read())
        file_object.write('\n\n'.encode())

        # cpp (絶対パス) => cpp (絶対パス): リンクは相対パスに
        self.file_class.depends = sorted(list(set(self.file_class.depends)))
        if self.file_class.depends != []:
            file_object.write('## Dependencies\n'.encode())
            for depends in self.file_class.depends:
                if depends not in path_to_verification:
                    raise FileNotFoundError('{} seems not to exist in path_to_verification'.format(depends))
                mark = self.get_mark(path_to_verification[depends])

                if depends not in path_to_title:
                    raise FileNotFoundError('{} seems not to exist in path_to_title'.format(depends))
                title = path_to_title[depends]

                link = self.get_link(self.get_destination(depends, 'library')) + '.html'
                file_object.write('* {} [{}]({})\n'.format(mark, title, link).encode())
            file_object.write('\n\n'.encode())

        # cpp <= cpp
        required_file_list = [f for f in self.file_class.required if not re.match(r'^.*\.test\.(cpp|hpp|cc)$', str(f))]
        required_file_list = sorted(list(set(required_file_list)))
        if required_file_list != []:
            file_object.write('## Required\n'.encode())
            for required in required_file_list:
                if required not in path_to_verification:
                    raise FileNotFoundError('{} seems not to exist in path_to_verification'.format(required))
                mark = self.get_mark(path_to_verification[required])

                if required not in path_to_title:
                    raise FileNotFoundError('{} seems not to exist in path_to_title'.format(required))
                title = path_to_title[required]

                link = self.get_link(self.get_destination(required, 'library')) + '.html'
                file_object.write('* {} [{}]({})\n'.format(mark, title, link).encode())
            file_object.write('\n\n'.encode())

        # cpp => test.cpp
        verified_file_list = [f for f in self.file_class.required if re.match(r'^.*\.test\.(cpp|hpp|cc)$', str(f))]
        verified_file_list = sorted(list(set(verified_file_list)))
        if verified_file_list != []:
            file_object.write('## Verified\n'.encode())
            for verified in verified_file_list:
                if verified not in path_to_verification:
                    raise FileNotFoundError('{} seems not to exist in path_to_verification'.format(verified))
                mark = self.get_mark(path_to_verification[verified])

                if verified not in path_to_title:
                    raise FileNotFoundError('{} seems not to exist in path_to_title'.format(verified))
                title = path_to_title[verified]

                link = self.get_link(self.get_destination(verified, 'verify')) + '.html'
                file_object.write('* {} [{}]({})\n'.format(mark, title, link).encode())
            file_object.write('\n\n'.encode())

        # source code
        file_object.write('## Code\n'.encode())
        file_object.write('```cpp\n'.encode())
        with open(self.file_class.file_path, 'rb') as f:
            file_object.write(f.read())
        file_object.write('\n```\n\n'.encode())

        # back to top
        file_object.write('[Back to top page]({})\n\n'.format(back_to_top_link).encode())

    def build(self, path_to_title: 'OrderedDict[pathlib.Path, str]', path_to_verification: Dict[pathlib.Path, bool], category: str, categorize: bool) -> None:
        self.make_directory()
        with open(str(self.destination) + '.md', mode='wb') as file_object:
            self.write_header(file_object)
            self.write_title(file_object, category, categorize)
            self.write_contents(file_object, path_to_title, path_to_verification)


class MarkdownTopPage(MarkdownPage):
    def __init__(self, cpp_source_path: pathlib.Path, md_destination_path: pathlib.Path, config: Dict[str, Any]) -> None:
        self.cpp_source_path = cpp_source_path.resolve()
        self.md_destination_path = md_destination_path.resolve()
        self.destination = md_destination_path / 'index'
        self.config = config

    def write_header(self, file_object: IO) -> None:
        file_object.write(assets_site_header_txt)
        self.include_js(file_object, self.md_destination_path / './assets/js/copy-button.js')
        self.include_css(file_object, self.md_destination_path / './assets/css/copy-button.css')
        file_object.write('\n\n'.encode())

    def write_title(self, file_object: IO) -> None:
        title = self.config.setdefault('title', 'C++ Competitive Programming Library')
        file_object.write('# {}\n\n'.format(title).encode())
        description = self.config.setdefault('description', '')
        if description != '': file_object.write('{}\n\n'.format(description).encode())
        toc = self.config.setdefault('toc', False)
        if toc:
            file_object.write('* this unordered seed list will be replaced by toc as unordered list\n'.encode())
            file_object.write('{:toc}\n\n'.encode())

    def write_contents(
            self,
            file_object: IO,
            verify_files: 'OrderedDict[pathlib.Path, CppFile]',
            library_files: 'OrderedDict[pathlib.Path, CppFile]',
            verify_category_to_path: 'OrderedDict[str, List[pathlib.Path]]',
            library_category_to_path: 'OrderedDict[str, List[pathlib.Path]]',
            path_to_title: 'OrderedDict[pathlib.Path, str]',
            path_to_verification: Dict[pathlib.Path, bool],
            categorize_verify: bool,
            categorize_library: bool,
    ) -> None:
        if categorize_library:
            if library_files != {}:
                file_object.write('## Library Files\n'.encode())
                for category, library_list in library_category_to_path.items():
                    file_object.write('### {}\n'.format(category).encode())
                    for library_file in library_list:
                        if library_file not in path_to_verification:
                            raise FileNotFoundError('{} seems not to exist in path_to_verification'.format(library_file))
                        mark = self.get_mark(path_to_verification[library_file])

                        if library_file not in path_to_title:
                            raise FileNotFoundError('{} seems not to exist in path_to_title'.format(library_file))
                        title = path_to_title[library_file]

                        link = self.get_link(self.get_destination(library_file, 'library')) + '.html'
                        file_object.write('* {} [{}]({})\n'.format(mark, title, link).encode())
                    file_object.write('\n\n'.encode())
        else:
            if library_files != {}:
                file_object.write('## Library Files\n'.encode())
                for library_file in library_files.keys():
                    if library_file not in path_to_verification:
                        raise FileNotFoundError('{} seems not to exist in path_to_verification'.format(library_file))
                    mark = self.get_mark(path_to_verification[library_file])

                    if library_file not in path_to_title:
                        raise FileNotFoundError('{} seems not to exist in path_to_title'.format(library_file))
                    title = path_to_title[library_file]

                    link = self.get_link(self.get_destination(library_file, 'library')) + '.html'
                    file_object.write('* {} [{}]({})\n'.format(mark, title, link).encode())
                file_object.write('\n\n'.encode())

        if categorize_verify:
            if verify_files != {}:
                file_object.write('## Verify Files\n'.encode())
                for category, verify_list in verify_category_to_path.items():
                    file_object.write('### {}\n'.format(category).encode())
                    for verify_file in verify_list:
                        if verify_file not in path_to_verification:
                            raise FileNotFoundError('{} seems not to exist in path_to_verification'.format(verify_file))
                        mark = self.get_mark(path_to_verification[verify_file])

                        if verify_file not in path_to_title:
                            raise FileNotFoundError('{} seems not to exist in path_to_title'.format(verify_file))
                        title = path_to_title[verify_file]

                        link = self.get_link(self.get_destination(verify_file, 'verify')) + '.html'
                        file_object.write('* {} [{}]({})\n'.format(mark, title, link).encode())
                    file_object.write('\n\n'.encode())
        else:
            if verify_files != {}:
                file_object.write('## Verify Files\n'.encode())
                for verify_file in verify_files.keys():
                    if verify_file not in path_to_verification:
                        raise FileNotFoundError('{} seems not to exist in path_to_verification'.format(verify_file))
                    mark = self.get_mark(path_to_verification[verify_file])

                    if verify_file not in path_to_title:
                        raise FileNotFoundError('{} seems not to exist in path_to_title'.format(verify_file))
                    title = path_to_title[verify_file]

                    link = self.get_link(self.get_destination(verify_file, 'verify')) + '.html'
                    file_object.write('* {} [{}]({})\n'.format(mark, title, link).encode())
                file_object.write('\n\n'.encode())

    def build(
            self,
            verify_files: 'OrderedDict[pathlib.Path, CppFile]',
            library_files: 'OrderedDict[pathlib.Path, CppFile]',
            verify_category_to_path: 'OrderedDict[str, List[pathlib.Path]]',
            library_category_to_path: 'OrderedDict[str, List[pathlib.Path]]',
            path_to_title: 'OrderedDict[pathlib.Path, str]',
            path_to_verification: Dict[pathlib.Path, bool],
            categorize_verify: bool,
            categorize_library: bool,
    ) -> None:
        self.make_directory()
        with open(str(self.destination) + '.md', mode='wb') as file_object:
            self.write_header(file_object)
            self.write_title(file_object)
            self.write_contents(
                file_object,
                verify_files,
                library_files,
                verify_category_to_path,
                library_category_to_path,
                path_to_title,
                path_to_verification,
                categorize_verify,
                categorize_library,
            )


class PagesBuilder:
    def __init__(self, cpp_source_pathstr: str, md_destination_pathstr: str = './md-output', config: Dict[str, Any] = {}) -> None:
        # ビルド対象ファイル一覧
        cpp_source_path = pathlib.Path(cpp_source_pathstr).resolve()
        md_destination_path = pathlib.Path(md_destination_pathstr).resolve()
        self.verify_files = self.get_files(cpp_source_path, r'^.*\.test\.(cpp|hpp|cc)$')
        self.library_files = self.get_files(cpp_source_path, r'^.*\.(cpp|hpp|cc)$', self.verify_files)

        # ファイルまでの絶対パス <-> タイトル
        self.title_to_path = self.map_title2path()
        self.path_to_title = self.map_path2title()

        # カテゴリ -> ファイルまでの絶対パスのリスト
        self.verify_category_to_path, self.library_category_to_path = self.map_category2path()

        # 設定項目
        self.config = config

        # 依存関係を調べる
        self.get_required()

        # ファイルまでの絶対パス -> Verification Status
        self.path_to_verification = self.map_path2verification()

        # ページをビルド
        self.build_verify_files(cpp_source_path, md_destination_path)
        self.build_library_files(cpp_source_path, md_destination_path)
        self.build_top_page(cpp_source_path, md_destination_path)
        self.build_assets(md_destination_path)
        self.build_static_files(md_destination_path)

    # ignore されるべきなら True
    def is_ignored(self, file_path: pathlib.Path) -> bool:
        parser = FileParser(file_path)
        ignore = []
        ignore.extend(parser.get_contents_by_tag(r'@ignore'))
        ignore.extend(parser.get_contents_by_tag(r'#define IGNORE'))
        return ignore != []

    # source_path 内にあって拡張子末尾が extension であるファイル一覧
    # ignored_files に含まれるならば無視
    def get_files(self, source_path: pathlib.Path, extension: str, ignored_files: 'OrderedDict[pathlib.Path, CppFile]' = OrderedDict()) -> 'OrderedDict[pathlib.Path, CppFile]':
        match_result = [p for p in source_path.glob(r'./**/*') if re.search(extension, str(p))]
        files = {}
        for matched_file in match_result:
            if any([matched_file.samefile(ignored_file) for ignored_file in ignored_files]):
                continue
            if not self.is_ignored(matched_file):
                matched_file = matched_file.resolve()
                files[matched_file] = CppFile(matched_file, source_path)
        files = OrderedDict(sorted(files.items(), key=lambda x: x[0]))
        return files

    # title の重複があったらナンバリング付与
    def map_title2path(self) -> 'OrderedDict[str, pathlib.Path]':
        title_cnt, title_num, result = {}, {}, {}  # type: Dict[str, int], Dict[str, int], Dict[str, pathlib.Path]
        for cpp_class in self.library_files.values():
            title_cnt.setdefault(cpp_class.title, 0)
            title_cnt[cpp_class.title] += 1
        for cpp_class in self.verify_files.values():
            title_cnt.setdefault(cpp_class.title, 0)
            title_cnt[cpp_class.title] += 1

        for cpp_class in self.library_files.values():
            title = cpp_class.title
            if title_cnt[title] >= 2:
                title_num.setdefault(title, 0)
                title_num[title] += 1
                title += '{:02}'.format(title_num[title])
            result[title] = cpp_class.file_path
        for cpp_class in self.verify_files.values():
            title = cpp_class.title
            if title_cnt[title] >= 2:
                title_num.setdefault(title, 0)
                title_num[title] += 1
                title += '{:02}'.format(title_num[title])
            result[title] = cpp_class.file_path
        return OrderedDict(sorted(result.items(), key=lambda x: x[0]))

    def map_path2title(self) -> 'OrderedDict[pathlib.Path, str]':
        result = {}
        for cpp_class in self.library_files.values():
            result[cpp_class.file_path] = cpp_class.title
        for cpp_class in self.verify_files.values():
            result[cpp_class.file_path] = cpp_class.title
        result = OrderedDict(sorted(result.items(), key=lambda x: x[0]))

        # verify_files, library_files のタイトルを振り直す
        for verify in self.verify_files.keys():
            self.verify_files[verify].title = result[verify]
        for library in self.library_files.keys():
            self.library_files[library].title = result[library]

        return result

    def map_category2path(self) -> Tuple['OrderedDict[str, List[pathlib.Path]]', 'OrderedDict[str, List[pathlib.Path]]']:
        verify_result, library_result = {}, {}  # type: Dict[str, List[pathlib.Path]], Dict[str, List[pathlib.Path]]
        for cpp_class in self.verify_files.values():
            verify_result.setdefault(cpp_class.category, [])
            verify_result[cpp_class.category].append(cpp_class.file_path)
        for file_path_list in verify_result.values():
            file_path_list.sort()
        verify_result_ordered = OrderedDict(sorted(verify_result.items(), key=lambda x: x[0]))

        for cpp_class in self.library_files.values():
            library_result.setdefault(cpp_class.category, [])
            library_result[cpp_class.category].append(cpp_class.file_path)
        for file_path_list in library_result.values():
            file_path_list.sort()
        library_result_ordered = OrderedDict(sorted(library_result.items(), key=lambda x: x[0]))
        return verify_result_ordered, library_result_ordered

    def get_required(self) -> None:
        map_required = {}  # type: Dict[pathlib.Path, List[pathlib.Path]]
        for cpp_class in self.library_files.values():
            for depends in cpp_class.depends:
                map_required.setdefault(depends, [])
                map_required[depends].append(cpp_class.file_path)
        for cpp_class in self.verify_files.values():
            for depends in cpp_class.depends:
                map_required.setdefault(depends, [])
                map_required[depends].append(cpp_class.file_path)

        for depends_list in map_required.values():
            depends_list.sort()

        for cpp_file in self.library_files.keys():
            map_required.setdefault(cpp_file, [])
            self.library_files[cpp_file].set_required(map_required[cpp_file])

        for cpp_file in self.verify_files.keys():
            map_required.setdefault(cpp_file, [])
            self.verify_files[cpp_file].set_required(map_required[cpp_file])

    def map_path2verification(self) -> Dict[pathlib.Path, bool]:
        result = {}  # type: Dict[pathlib.Path, bool]
        # .test.cpp の verify 状況確認
        for cpp_file, cpp_class in self.verify_files.items():
            result[cpp_file] = cpp_class.is_verified

        # .cpp は、それを必要としている .test.cpp が少なくとも 1 つ存在し
        # 全ての .test.cpp が verify 済みなら OK
        for cpp_file, cpp_class in self.library_files.items():
            verify_file_cnt, cond = 0, True
            for verify in cpp_class.required:
                if re.match(r'^.*\.test\.(cpp|hpp|cc)$', str(verify)):
                    verify_file_cnt += 1
                    cond = cond and result[verify]
            result[cpp_file] = (verify_file_cnt > 0 and cond)
        return result

    def build_verify_files(self, cpp_source_path: pathlib.Path, md_destination_path: pathlib.Path) -> None:
        for category, verify_path_list in self.verify_category_to_path.items():
            for matched_file_path in verify_path_list:
                verify_file_class = self.verify_files[matched_file_path]
                page = MarkdownArticle(verify_file_class, 'verify', cpp_source_path, md_destination_path)
                html_cond = self.config.setdefault('html', False)
                categorize_verify_cond = self.config.setdefault('categorize_verify', False)
                page.build(self.path_to_title, self.path_to_verification, category, categorize_verify_cond)
                if html_cond: page.convert_to_html()

    def build_library_files(self, cpp_source_path: pathlib.Path, md_destination_path: pathlib.Path) -> None:
        for category, library_path_list in self.library_category_to_path.items():
            for matched_file_path in library_path_list:
                library_file_class = self.library_files[matched_file_path]
                page = MarkdownArticle(library_file_class, 'library', cpp_source_path, md_destination_path)
                html_cond = self.config.setdefault('html', False)
                categorize_library_cond = self.config.setdefault('categorize_library', True)
                page.build(self.path_to_title, self.path_to_verification, category, categorize_library_cond)
                if html_cond: page.convert_to_html()

    def build_top_page(self, cpp_source_path: pathlib.Path, md_destination_path: pathlib.Path) -> None:
        page = MarkdownTopPage(cpp_source_path, md_destination_path, self.config)
        html_cond = self.config.setdefault('html', False)
        categorize_verify_cond = self.config.setdefault('categorize_verify', False)
        categorize_library_cond = self.config.setdefault('categorize_library', True)
        page.build(
            self.verify_files,
            self.library_files,
            self.verify_category_to_path,
            self.library_category_to_path,
            self.path_to_title,
            self.path_to_verification,
            categorize_verify_cond,
            categorize_library_cond,
        )
        if html_cond: page.convert_to_html()

    def build_assets(self, md_destination_path: pathlib.Path) -> None:
        assets_dir = md_destination_path / 'assets'
        if assets_dir.exists():
            shutil.rmtree(str(assets_dir))
        for asset in deployed_assets:
            path = md_destination_path / asset['path']  # type: ignore
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(str(path), 'wb') as fh:
                fh.write(asset['data'])  # type: ignore

    def build_static_files(self, md_destination_path: pathlib.Path) -> None:
        static_dir = pathlib.Path('.verify-helper/docs/static')
        for src_path in map(pathlib.Path, glob.glob(str(static_dir) + '/**/*', recursive=True)):
            dst_path = md_destination_path / src_path.relative_to(static_dir)
            if src_path.is_file():
                shutil.copyfile(str(src_path), str(dst_path))


def main(*, html: bool = True) -> None:
    # 実行テスト
    config = {
        'title': 'ライブラリの HTML ビルドテスト',  # title of top page
        'description': 'ここに書いた内容がトップページに足されます',  # description of top page
        'toc': True,  # table of contents (default: False)
        'html': html,  # generate HTML as well as Markdown (default: True)
        'categorize_library': True,  # show library files with categorizing (default: True)
        'categorize_verify': False,  # show verify files with categorizing (default: False)
    }
    builder = PagesBuilder(cpp_source_pathstr='.', config=config)


if __name__ == '__main__':
    main()
