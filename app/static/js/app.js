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
        if (_previewTitle.length > 0 && _previewContent.length > 0) {
            _previewTitle.text(title);
            _previewContent.html(marked(content));
            _previewContent.find('img').each(function() {
                $(this).addClass('img-responsive');
            });
        }
    }

    _title.on('keyup', function() {
        setPreview(_title.val(), _content.val())
    });
    _content.on('keyup', function() {
        setPreview(_title.val(), _content.val())
    });
    if (_title.length > 0 && _content.length > 0) {
        setPreview(_title.val(), _content.val())
    }

    if ($('.comment-reply-btn').length > 0) {
        $('.comment-reply-btn').on('click', function(e) {
            e.preventDefault();
            $(this).parent().next('.comment-reply').fadeToggle();
        });
    }
});