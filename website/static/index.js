// takes the noteID we pass, send a post request to the deleteNote endpoint. once we get a response, reload the window
function deleteNote(noteID) {
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({ noteID: noteID})
    }).then((_res) => {
        // reload the page
        window.location.href = "/"
    })
}