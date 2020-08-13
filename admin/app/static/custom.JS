// This starts a markdown editor instance for each textarea marked with the
// markdownEditor class will only work on Flask-Admin views that have
// the extra_js and extra_css fields that include this file and the SimpleMDE
// cdn links

// hardcoded for now but adds onclick event of Scene conversation editor
// to show MDE instead of standard textarea
document.getElementById("conversation_content-button").addEventListener("click", replace_TextAreas);
window.onload=replace_TextAreas;

function replace_TextAreas(){
    textareas = [...document.getElementsByClassName('markdownEditor')];

    textareas.forEach((textarea) => {
      new SimpleMDE({
                element: textarea,
                autoDownloadFontAwesome: true,
                spellChecker: false,
                forceSync: true,
            });
      textarea.classList.remove("markdownEditor")
      });
}
