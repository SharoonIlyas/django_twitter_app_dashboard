
function getCookie(name) 
{
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');
window.onload=function()
{
    var form = document.getElementById('#form-id')
    if(form){

        form.addEventListener('submit', function(e)
        {
            e.preventDefault()
            console.log('Form submitted')
            var url = 'http://127.0.0.1:8000/api/tweet-create/'
            
            var text = document.getElementById('title').value
            fetch(url, 
            {
                method:'POST',
                headers:
                {
                    'Content-type':'application/json',
                    'X-CSRFToken':csrftoken,
                },
                body:JSON.stringify({'text': text })
            }
    
            )
            .then(function(response)
                {
                    console.log(response)  
                    document.getElementById('form-id').reset()
                    $("#wrapper").load(location.href + " #wrapper");
    
            })
        })
    }
    
   
    
}





$(document).ready(function(){
    $(document).on('click', '.deletebtn', function(){
        var productId = this.dataset.articleid
        deleteItem(productId)
        
    })
})


$(document).ready(function(){
    $(document).on('click', '.follow_button', function(){
        var username = this.dataset.user
        var action  = this.dataset.action

        followToggle(username, action)
        console.log({'username':username , 'action':action  })
        
    })
})

function followToggle(user_name, action)
{
    fetch(`http://127.0.0.1:8000/api/profile/${user_name}/follow/`, {
                method:'POST', 
                headers:{
                    'Content-type':'application/json',
                    'X-CSRFToken':csrftoken,
                },

                body:JSON.stringify({'action': action})
                
            }).then((response)=>{
                console.log(response)
               return response.json()
            })
            
            .then((data)=>{
                console.log(data)
                $("#followed_row").load(location.href + " #followed_row");
                $("#find_followed_row").load(location.href + " #find_followed_row");

            })
        
}


        
        





function deleteItem(id){
            console.log('Delete clicked')
            fetch(`http://127.0.0.1:8000/api/tweet-delete/${id}/`, {
                method:'DELETE', 
                headers:{
                    'Content-type':'application/json',
                    'X-CSRFToken':csrftoken,
                }
            }).then((response) => {
                return response.json()
                
            }).then((data)=>
            {

                $("#wrapper").load(location.href + " #wrapper");

            })
        }


