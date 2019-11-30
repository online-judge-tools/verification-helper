window.addEventListener('load', function(){
  /// コピーテキストボタンを実装
  $('.highlight > .highlight > code').each(function(index, element) {
      $(element).parent().parent().css('position', 'relative');
      $(element).append('<button type="button" class="code-copy-btn" title="Copied!">Copy</button>');
  });

  $('.highlight > .highlight > code > button').on('click',function(){
    /// テキスト要素を選択＆クリップボードにコピー
    var textElem = $(this).parent();
    window.getSelection().selectAllChildren(textElem[0]);
    document.execCommand("copy");
    window.getSelection().removeAllRanges();
    
    /// コピー完了した後の処理
    /// トースト通知と化すると親切かも...\
    $('.highlight > .highlight > code > button').showBalloon()
    setTimeout(function() {
      $('.highlight > .highlight > code > button').hideBalloon()
    }, 500);
  });
});

