var followBotton = document.getElementById("follow-button");
    followBotton.addEventListener("click", function(){
        fetch('{% url "social:follow" %}', {
        method: 'POST',
        body: JSON.stringify({
            user_id: "{{ user.id }}"
        }),
        headers: {'Content-Type': 'application/json', 'x-requested-with': 'XMLHttpRequest', 'X-CSRFToken': '{{csrf_token}}'}
        
    }).then(res => res.json()).then(function(data){
            if(data.follow){
                followBotton.textContent = "unFollow";
            } else {
                followBotton.textContent = "Follow";
            }
    })})