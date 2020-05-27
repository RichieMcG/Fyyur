const venueDeleteButton = document.querySelector('#venueDelete')
venueDeleteButton.addEventListener('click', function clickhandler(e) {
    if (window.confirm("Do you really want to delete this venue?")) {
        const venueToDelete = e.target.dataset['id']
        fetch(`/venues/${venueToDelete}`, {
            method: 'DELETE'
        }).then(res => {
            if (res.ok) {
                window.location.href = '/'
            }
    })
    .catch(e => console.error("ERROR", e))
    }
})

