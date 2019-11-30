# -*- coding: utf-8 -*-
import collections
import glob
import os
import pathlib
import re
import shutil

import markdown
import pkg_resources

package = 'onlinejudge_verify.data'
assets_site_header_txt = pkg_resources.resource_string(package, 'assets/site-header.txt')
deployed_assets = [
    {
        'path': pathlib.Path('css/copy-button.css'),
        'data': pkg_resources.resource_string(package, 'assets/css/copy-button.css'),
    },
    {
        'path': pathlib.Path('js/copy-button.js'),
        'data': pkg_resources.resource_string(package, 'assets/js/copy-button.js'),
    },
    {
        'path': pathlib.Path('_config.yml'),
        'data': pkg_resources.resource_string(package, 'assets/_config.yml'),
    },
]


class FileParser:
    # ファイルパスをもらって、行ごとに分ける
    def __init__(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError('{} does not exist'.format(file_path))
        with open(file_path) as f:
            self.lines = [line.strip() for line in f.readlines()]

    # タグをもらって、コンテンツの配列を出す
    def get_contents_by_tag(self, tag_name, l_pat='', r_pat=''):
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

    def get_implicit_dependencies(self):
        reg1 = r'^#include[ ]*".*".*$'
        matches = [line for line in self.lines if re.match(reg1, line)]
        reg2 = r'^#include[ ]*"(.*)".*$'
        results = [re.sub(reg2, r'\1', line).strip() for line in matches]
        return results


# 現状は C++ のみのサポートを考える
class CppFile:
    def __init__(self, file_path, source_path):
        self.file_path = os.path.normpath(file_path)
        self.source_path = source_path
        self.parser = FileParser(file_path)

        # file 指定が空なら、ファイルパスをタイトルにする
        self.title = self.parser.get_contents_by_tag(r'@file')
        if self.title == []:
            self.title = self.file_path
        else:
            # @title が複数あるなら最後を採用？？
            self.title = self.title[-1]

        self.brief = self.parser.get_contents_by_tag(r'@brief')
        self.brief.extend(self.parser.get_contents_by_tag(r'#define DESCRIPTION', r'"', r'"'))

        # category 指定が空なら、ディレクトリ名をカテゴリにする
        self.category = self.parser.get_contents_by_tag(r'@category')
        self.category.extend(self.parser.get_contents_by_tag(r'#define CATEGORY', r'"', r'"'))
        if self.category == []:
            self.category = os.path.dirname(self.file_path)
        else:
            self.category = self.category[-1]

        self.see = self.parser.get_contents_by_tag(r'@see')
        self.see.extend(self.parser.get_contents_by_tag(r'#define PROBLEM', r'"', r'"'))

        self.docs = self.parser.get_contents_by_tag(r'@docs')
        self.docs.extend(self.parser.get_contents_by_tag(r'#define DOCS', r'"', r'"'))

        self.depends = self.parser.get_contents_by_tag(r'@depends')
        self.depends.extend(self.parser.get_implicit_dependencies())
        self.depends.extend(self.parser.get_contents_by_tag(r'#define REQUIRES', r'"', r'"'))
        self.depends = self.to_source_relpath(self.depends)

        self.required = []
        self.is_verified = self.get_verification_status()

    def get_verification_status(self):
        return False  # [TODO]

    def to_source_relpath(self, item_list):
        result, file_dir = [], os.path.dirname(self.file_path)
        for item in item_list:
            relpath_from_source = os.path.join(file_dir, item)
            result.append(os.path.normpath(relpath_from_source))
        return result

    def set_required(self, required_list):
        self.required = required_list


class MarkdownPage:
    # requires: self.cpp_source_path, self.md_destination_path, self.destination
    def get_mark(self, cond):
        if cond:
            return ':heavy_check_mark:'
        else:
            return ':warning:'

    def get_destination(self, file_path, file_type=''):
        dst_file_dir, file_name = os.path.split(file_path)
        dst_file_dir = os.path.relpath(dst_file_dir or '.', self.cpp_source_path)
        md_file_dir = os.path.normpath(os.path.join(self.md_destination_path, file_type, dst_file_dir), )
        return os.path.join(md_file_dir, file_name)

    def get_link(self, link_href):
        return os.path.normpath(os.path.relpath(link_href, os.path.dirname(self.destination))) + '.html'

    def make_directory(self):
        dir_name, file_name = os.path.split(self.destination)
        os.makedirs(dir_name, exist_ok=True)

    def include_js(self, file_object, js_file_name):
        js_file_name = os.path.relpath(js_file_name, os.path.dirname(self.destination))
        html = '<script type="text/javascript" src="{}"></script>\n'.format(js_file_name)
        file_object.write(html)

    def include_css(self, file_object, css_file_name):
        css_file_name = os.path.relpath(css_file_name, os.path.dirname(self.destination))
        html = '<link rel="stylesheet" href="{}" />\n'.format(css_file_name)
        file_object.write(html)

    def convert_to_html(self):
        md_destination = self.destination + '.md'
        html_destination = self.destination + '.html'
        data = markdown.markdownFromFile(input=md_destination, output=html_destination, encoding="utf-8", extensions=['fenced_code', 'tables'])


class MarkdownArticle(MarkdownPage):
    def __init__(self, file_class, file_type, cpp_source_path, md_destination_path):
        self.file_class = file_class
        self.md_destination_path = md_destination_path
        self.cpp_source_path = cpp_source_path
        self.destination = self.get_destination(self.file_class.file_path, file_type)
        self.mark = self.get_mark(self.file_class.is_verified)

    # include (mathjax, js, css)
    def write_header(self, file_object):
        file_object.buffer.write(assets_site_header_txt)
        self.include_js(file_object, os.path.join(self.md_destination_path, './assets/js/copy-button.js'))
        self.include_css(file_object, os.path.join(self.md_destination_path, './assets/css/copy-button.css'))
        file_object.write('\n\n')

    def write_title(self, file_object, category, categorize):
        file_object.write('# {} {}\n'.format(self.mark, self.file_class.title))
        if categorize: file_object.write('* category: {}\n'.format(category))
        file_object.write('\n\n')

    def write_contents(self, file_object, path_to_title, path_to_verification):
        back_to_top_link = os.path.relpath(os.path.join(self.md_destination_path, 'index.html'), os.path.dirname(self.destination))

        file_object.write('[Back to top page]({})\n\n'.format(back_to_top_link))

        # brief, see, docs
        for brief in self.file_class.brief:
            file_object.write('* {}\n'.format(brief))
        for see in self.file_class.see:
            file_object.write('* see: [{}]({})\n'.format(see, see))
        for docs in self.file_class.docs:
            docs = os.path.join(os.path.dirname(self.file_class.file_path), docs)
            with open(docs) as f:
                file_object.write(f.read())
        file_object.write('\n\n')

        # cpp => cpp
        self.file_class.depends = sorted(list(set(self.file_class.depends)))
        if self.file_class.depends != []:
            file_object.write('## Dependencies\n')
            for depends in self.file_class.depends:
                mark = self.get_mark(path_to_verification[depends])
                title = path_to_title[depends]
                link = self.get_link(self.get_destination(depends, 'library'))
                file_object.write('* {} [{}]({})\n'.format(mark, title, link))
            file_object.write('\n\n')

        # cpp <= cpp
        required_file_list = [f for f in self.file_class.required if not re.match(r'^.*\.test\.(cpp|hpp|cc)$', f)]
        required_file_list = sorted(list(set(required_file_list)))
        if required_file_list != []:
            file_object.write('## Required\n')
            for required in required_file_list:
                mark = self.get_mark(path_to_verification[required])
                title = path_to_title[required]
                file_type = 'verify' if re.match(r'^.*\.test\.(cpp|hpp|cc)$', required) else 'library'
                link = self.get_link(self.get_destination(required, file_type))
                file_object.write('* {} [{}]({})\n'.format(mark, title, link))
            file_object.write('\n\n')

        # cpp => test.cpp
        verified_file_list = [f for f in self.file_class.required if re.match(r'^.*\.test\.(cpp|hpp|cc)$', f)]
        verified_file_list = sorted(list(set(verified_file_list)))
        if verified_file_list != []:
            file_object.write('## Verified\n')
            for verified in verified_file_list:
                mark = self.get_mark(path_to_verification[verified])
                title = path_to_title[verified]
                link = self.get_link(self.get_destination(verified, 'verify'))
                file_object.write('* {} [{}]({})\n'.format(mark, title, link))
            file_object.write('\n\n')

        # source code
        file_object.write('## Code\n')
        file_object.write('```cpp\n')
        with open(self.file_class.file_path) as f:
            file_object.write(f.read())
        file_object.write('\n```\n\n')

        # back to top
        file_object.write('[Back to top page]({})\n\n'.format(back_to_top_link))

    def build(self, path_to_title, path_to_verification, category, categorize):
        self.make_directory()
        with open(self.destination + '.md', mode="w") as file_object:
            self.write_header(file_object)
            self.write_title(file_object, category, categorize)
            self.write_contents(file_object, path_to_title, path_to_verification)


class MarkdownTopPage(MarkdownPage):
    def __init__(self, cpp_source_path, md_destination_path, config):
        self.cpp_source_path = cpp_source_path
        self.md_destination_path = md_destination_path
        self.destination = os.path.join(md_destination_path, 'index')
        self.config = config

    def write_header(self, file_object):
        file_object.buffer.write(assets_site_header_txt)
        self.include_js(file_object, os.path.join(self.md_destination_path, './assets/js/copy-button.js'))
        self.include_css(file_object, os.path.join(self.md_destination_path, './assets/css/copy-button.css'))
        file_object.write('\n\n')

    def write_title(self, file_object):
        title = self.config.setdefault('title', 'C++ Competitive Programming Library')
        file_object.write('# {}\n\n'.format(title))
        description = self.config.setdefault('description', '')
        if description != '': file_object.write('{}\n\n'.format(description))
        toc = self.config.setdefault('toc', False)
        if toc:
            file_object.write('* this unordered seed list will be replaced by toc as unordered list\n')
            file_object.write('{:toc}\n\n')

    def write_contents(
            self,
            file_object,
            verify_files,
            library_files,
            verify_category_to_path,
            library_category_to_path,
            path_to_title,
            path_to_verification,
            categorize_verify,
            categorize_library,
    ):
        if categorize_library:
            if library_files != {}:
                file_object.write('## Library Files\n')
                for category, library_list in library_category_to_path.items():
                    file_object.write('### {}\n'.format(category))
                    for library_file in library_list:
                        mark = self.get_mark(path_to_verification[library_file])
                        title = path_to_title[library_file]
                        link = self.get_link(self.get_destination(library_file, 'library'))
                        file_object.write('* {} [{}]({})\n'.format(mark, title, link))
                    file_object.write('\n\n')
        else:
            if library_files != {}:
                file_object.write('## Library Files\n')
                for library_file in library_files.keys():
                    mark = self.get_mark(path_to_verification[library_file])
                    title = path_to_title[library_file]
                    link = self.get_link(self.get_destination(library_file, 'library'))
                    file_object.write('* {} [{}]({})\n'.format(mark, title, link))
                file_object.write('\n\n')

        if categorize_verify:
            if verify_files != {}:
                file_object.write('## Verify Files\n')
                for category, verify_list in verify_category_to_path.items():
                    file_object.write('### {}\n'.format(category))
                    for verify_file in verify_list:
                        mark = self.get_mark(path_to_verification[verify_file])
                        title = path_to_title[verify_file]
                        link = self.get_link(self.get_destination(verify_file, 'verify'))
                        file_object.write('* {} [{}]({})\n'.format(mark, title, link))
                    file_object.write('\n\n')
        else:
            if verify_files != {}:
                file_object.write('## Verify Files\n')
                for verify_file in verify_files.keys():
                    mark = self.get_mark(path_to_verification[verify_file])
                    title = path_to_title[verify_file]
                    link = self.get_link(self.get_destination(verify_file, 'verify'))
                    file_object.write('* {} [{}]({})\n'.format(mark, title, link))
                file_object.write('\n\n')

    def build(
            self,
            verify_files,
            library_files,
            verify_category_to_path,
            library_category_to_path,
            path_to_title,
            path_to_verification,
            categorize_verify,
            categorize_library,
    ):
        self.make_directory()
        with open(self.destination + '.md', mode="w") as file_object:
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
    def __init__(self, cpp_source_path, md_destination_path='./md-output', config={}):
        self.verify_files = self.get_files(cpp_source_path, r'^.*\.test\.(cpp|hpp|cc)$')
        self.library_files = self.get_files(cpp_source_path, r'^.*\.(cpp|hpp|cc)$', self.verify_files)
        self.title_to_path = self.map_title2path()
        self.path_to_title = self.map_path2title()
        self.verify_category_to_path, self.library_category_to_path = self.map_category2path()
        self.config = config
        self.get_required()
        self.path_to_verification = self.map_path2verification()
        self.build_verify_files(cpp_source_path, md_destination_path)
        self.build_library_files(cpp_source_path, md_destination_path)
        self.build_top_page(cpp_source_path, md_destination_path)
        self.build_assets(md_destination_path)
        self.build_static_files(md_destination_path)

    # ignore が付いているか？
    def is_ignored(self, file_path):
        parser = FileParser(file_path)
        ignore = []
        ignore.extend(parser.get_contents_by_tag(r'@ignore'))
        ignore.extend(parser.get_contents_by_tag(r'#define IGNORE'))
        return ignore != []

    def get_files(self, source_path, extension, ignored_files={}):
        path = source_path + r'/**/*'
        match_result = [p for p in glob.glob(path, recursive=True) if re.search(extension, p)]
        files = {}
        for matched_file in match_result:
            if any([os.path.realpath(matched_file) == os.path.realpath(ignored_file) for ignored_file in ignored_files]):
                continue
            if not self.is_ignored(matched_file):
                matched_file = os.path.normpath(matched_file)
                files[matched_file] = CppFile(matched_file, source_path)
        files = collections.OrderedDict(sorted(files.items(), key=lambda x: x[0]))
        return files

    # title の重複があったらナンバリング付与
    def map_title2path(self):
        title_cnt, title_num, result = {}, {}, {}
        for cpp_class in dict(**self.library_files, **self.verify_files).values():
            title_cnt.setdefault(cpp_class.title, 0)
            title_cnt[cpp_class.title] += 1

        for cpp_class in dict(**self.library_files, **self.verify_files).values():
            title = cpp_class.title
            if title_cnt[title] >= 2:
                title_num.setdefault(title, 0)
                title_num[title] += 1
                title += '{:02}'.format(title_num[title])
            result[title] = cpp_class.file_path
        result = collections.OrderedDict(sorted(result.items(), key=lambda x: x[0]))
        return result

    def map_path2title(self):
        result = {}
        for cpp_class in dict(**self.library_files, **self.verify_files).values():
            result[cpp_class.file_path] = cpp_class.title
        result = collections.OrderedDict(sorted(result.items(), key=lambda x: x[0]))
        return result

    def map_category2path(self):
        verify_result, library_result = {}, {}
        for cpp_class in self.verify_files.values():
            verify_result.setdefault(cpp_class.category, [])
            verify_result[cpp_class.category].append(cpp_class.file_path)
        for file_path_list in verify_result.values():
            file_path_list.sort()
        verify_result = collections.OrderedDict(sorted(verify_result.items(), key=lambda x: x[0]))

        for cpp_class in self.library_files.values():
            library_result.setdefault(cpp_class.category, [])
            library_result[cpp_class.category].append(cpp_class.file_path)
        for file_path_list in library_result.values():
            file_path_list.sort()
        library_result = collections.OrderedDict(sorted(library_result.items(), key=lambda x: x[0]))
        return verify_result, library_result

    def get_required(self):
        map_required = {}
        for cpp_class in dict(**self.library_files, **self.verify_files).values():
            for depends in cpp_class.depends:
                map_required.setdefault(depends, [])
                map_required[depends].append(cpp_class.file_path)

        for cpp_file in self.library_files.keys():
            map_required.setdefault(cpp_file, [])
            self.library_files[cpp_file].set_required(map_required[cpp_file])

        for cpp_file in self.verify_files.keys():
            map_required.setdefault(cpp_file, [])
            self.verify_files[cpp_file].set_required(map_required[cpp_file])

    def map_path2verification(self):
        result = {}
        # .test.cpp の verify 状況確認
        for cpp_file, cpp_class in self.verify_files.items():
            result[cpp_file] = cpp_class.is_verified

        # .cpp は、それを必要としている .test.cpp が少なくとも 1 つ存在し
        # 全ての .test.cpp が verify 済みなら OK
        for cpp_file, cpp_class in self.library_files.items():
            verify_file_cnt, cond = 0, True
            for verify in cpp_class.required:
                if re.match(r'^.*\.test\.(cpp|hpp|cc)$', verify):
                    verify_file_cnt += 1
                    cond &= result[verify]
            result[cpp_file] = (verify_file_cnt > 0 and cond)
        return result

    def build_verify_files(self, cpp_source_path, md_destination_path):
        for category, verify_path_list in self.verify_category_to_path.items():
            for matched_file_path in verify_path_list:
                verify_file_class = self.verify_files[matched_file_path]
                page = MarkdownArticle(verify_file_class, 'verify', cpp_source_path, md_destination_path)
                html_cond = self.config.setdefault('html', False)
                categorize_verify_cond = self.config.setdefault('categorize_verify', False)
                page.build(self.path_to_title, self.path_to_verification, category, categorize_verify_cond)
                if html_cond: page.convert_to_html()

    def build_library_files(self, cpp_source_path, md_destination_path):
        for category, library_path_list in self.library_category_to_path.items():
            for matched_file_path in library_path_list:
                library_file_class = self.library_files[matched_file_path]
                page = MarkdownArticle(library_file_class, 'library', cpp_source_path, md_destination_path)
                html_cond = self.config.setdefault('html', False)
                categorize_library_cond = self.config.setdefault('categorize_library', True)
                page.build(self.path_to_title, self.path_to_verification, category, categorize_library_cond)
                if html_cond: page.convert_to_html()

    def build_top_page(self, cpp_source_path, md_destination_path):
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

    def build_assets(self, md_destination_path):
        assets_dir = pathlib.Path(md_destination_path) / 'assets'
        if assets_dir.exists():
            shutil.rmtree(str(assets_dir))
        for asset in deployed_assets:
            path = pathlib.Path(md_destination_path) / asset['path']
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(str(path), 'wb') as fh:
                fh.write(asset['data'])

    def build_static_files(self, md_destination_path):
        static_dir = pathlib.Path('.verify-helper/docs/static')
        for src_path in map(pathlib.Path, glob.glob(str(static_dir) + '/**/*', recursive=True)):
            dst_path = pathlib.Path(md_destination_path) / src_path.relative_to(static_dir)
            if src_path.is_file():
                shutil.copyfile(str(src_path), str(dst_path))


def main(*, html=True):
    # 実行テスト
    config = {
        'title': 'ライブラリの HTML ビルドテスト',  # title of top page
        'description': 'ここに書いた内容がトップページに足されます',  # description of top page
        'toc': True,  # table of contents (default: False)
        'html': html,  # generate HTML as well as Markdown (default: True)
        'categorize_library': True,  # show library files with categorizing (default: True)
        'categorize_verify': False,  # show verify files with categorizing (default: False)
    }
    builder = PagesBuilder(cpp_source_path='.', config=config)


if __name__ == '__main__':
    main()
