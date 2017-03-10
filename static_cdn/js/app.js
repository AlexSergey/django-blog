$(function() {
    var postImages = $('.post-detail-item img');

    if (postImages.length > 0) {
        postImages.each(function() {
            $(this).addClass('img-responsive');
        });
    }

    var _title = $('#id_title');
    var _content = $('#id_content');
    var _previewTitle = $('#preview-title');
    var _previewContent = $('#preview-content');


    function setPreview(title, content) {
        _previewTitle.text(title);
        _previewContent.html(marked(content));
        _previewContent.find('img').each(function() {
            $(this).addClass('img-responsive');
        });
    }

    _title.on('keyup', function() {
        setPreview(_title.val(), _content.val())
    });
    _content.on('keyup', function() {
        setPreview(_title.val(), _content.val())
    });
    setPreview(_title.val(), _content.val())
});