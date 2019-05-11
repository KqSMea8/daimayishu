function set_resource_word() {
    key_word = $("#key_word_input").val()
    $("#key_word_btn").attr("href", "/resource/index?key_word=" + key_word)
}

function set_blog_word() {
    key_word = $("#key_word_input").val()
    $("#key_word_btn").attr("href", "/blog/index?key_word=" + key_word)
}

function set_advisory_word() {
    key_word = $("#key_word_input").val()
    $("#key_word_btn").attr("href", "/advisory/index?key_word=" + key_word)
}
