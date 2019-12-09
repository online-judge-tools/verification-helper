window.addEventListener('load', function(){
    // コピーテキストボタンを実装
    $('pre > code').each(function(index, element) {
        $(element).parent().wrap('<div style="position: relative;"></div>');
        $(element).parent().parent().append('<button type="button" class="code-copy-btn" title="Copied!">Copy</button>');
    });

    $('div > button').on('click',function(){
        // テキスト要素を選択＆クリップボードにコピー
        var textElem = $(this).siblings(':first');
        window.getSelection().selectAllChildren(textElem[0]);
        document.execCommand("copy");
        window.getSelection().removeAllRanges();
        
        // コピー完了した後の処理
        // トースト通知とかすると親切かも...
        $(this).showBalloon();
        const this_ = this;
        setTimeout(function() {
            $(this_).hideBalloon();
        }, 300);
    });
});
