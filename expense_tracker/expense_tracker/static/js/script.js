(
    function () {

        var input = document.querySelector('#tagInput');

        if (input) {
            input.addEventListener('keydown', function (e) {
                if (e.keyCode != 13) {
                    return;
                }

                e.preventDefault()

                if (this.value == '') {
                    return;
                }

                var tagName = this.value.toLowerCase();
                this.value = ''

                addNewTag(tagName)
                updateTagsString()
            })
        }

        function addNewTag(tagName) {

            tags = fetchTagArray()

            if (tags.includes(tagName)){
                return;
            }

            document.querySelector('#tagsContainer').insertAdjacentHTML('beforeend',
                `<li class="tag">
                    <span class="name mr-1">${tagName}</span>
                    <span onclick="removeTag(this)" class="btnRemove bold">X</span>
                </li>`)
        }

    }
)()

function fetchTagArray() {

    tags = []

    document.querySelectorAll('.tag').forEach(function (e) {
        tagNameText = e.querySelector('.name').innerHTML.toLowerCase();
        tags.push(tagNameText)
    })

    return tags
}

function updateTagsString() {
    tags = fetchTagArray()
    document.querySelector('#tagsString').value = tags.join(',')
}

function removeTag(e) {
    e.parentElement.remove()
    updateTagsString()
}