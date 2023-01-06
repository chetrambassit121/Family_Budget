(function(){
	document.querySelector('#categoryInput').addEventListener('keydown', function(e){
		if (e.keyCode != 13){
			return;
		}

		e.preventDefault()

		var categoryName = this.value 
		this.value = ''
		addNewCategory(categoryName)
		updateCategoriesString()
	})

	function addNewCategory(name){
		document.querySelector('#categoriesContainer').insertAdjacentHTML('beforeend', 
		`<li class="category">
			<span class="name">${name}</span>
			<span onclick="removeCategory(this)" style="cursor:pointer" class="btnRemove bold">X</span>
		</li>`)
	}

})()

function fetchCategoryArray(){
	var categories = []
	document.querySelectorAll('.category').forEach(function(e){
		name = e.querySelector('.name').innerHTML 
		if (name == '') return
		categories.push(name)
	})
	return categories
}

function updateCategoriesString(){
	categories = fetchCategoryArray()
	document.querySelector('input[name="categoriesString"]').value = categories.join(',')
}


function removeCategory(e){
	e.parentElement.remove()
	updateCategoriesString()
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}






// <script>
//     $(document).ready(function(e) {
//         // messages timeout for 10 sec 
//         setTimeout(function() {
//             $('.fade-messages').fadeOut('slow');
//         }, 1000); // <-- time in milliseconds, 1000 =  1 sec

//         // delete message
//         $('.del-msg').live('click',function(){
//             $('.del-msg').parent().attr('style', 'display:none;');
//         })
//     });
// </script>