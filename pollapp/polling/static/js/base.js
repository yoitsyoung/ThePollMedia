document.addEventListener('DOMContentLoaded',() => {
    
    loadQuestion(3);
})

// If no question_id is provided, get a random question
function loadQuestion(question_id='random'){
    const xhr = new XMLHttpRequest()
    const questionBlock = document.querySelector('.question-content')
    
    xhr.open('GET',`questions/${question_id}`)
    xhr.onload = () => {
        const content = JSON.parse(xhr.responseText);
        console.log(content)
        // Add in new innerhtml
        var question = 
        `
        <div id="question_title"><h6>${content['title']}</h6></div>
        <div id="question_content"><p>${content['content']}</p></div>
        `
        var optionText = ''
        optionArray = content['options']
        for (var i = 0; i < optionArray.length; i++){
            optionText +=
            `
            <form class = 'option_form' method = 'POST' action = '/answer_question'>
                <input type='hidden' name='csrfmiddlewaretoken' value='${CSRF_TOKEN}'>
                <input type='hidden' name = 'id' value='${optionArray[i]['id']}'>
                <span><input type = 'submit' class = 'btn btn-primary' value = '${optionArray[i]["content"]}' ></span>
            </form>
            <span class='score' style = 'display:none;'>${optionArray[i]['score']}</span>
            `
        
        }
        var questionHTML = question + optionText
        questionBlock.innerHTML = questionHTML

        // ajax 
        $(".option_form").submit(function(e){
            console.log('ajax kicking in')
            e.preventDefault();
            console.log($(this))
            var url=$(this).attr('action');
            var serializedData=$(this).closest('form').serialize();
            // add one to score
            var scoreboard=$(this).next('span')[0]
            console.log(scoreboard)
            var score = parseInt(scoreboard.innerHTML)
            console.log(score)
            score += 1
            scoreboard.innerHTML = score.toString()
            var profileScore = parseFloat($('#profileScore')[0].innerHTML)
            console.log(profileScore)
            profileScore += 1.0
            $('#profileScore')[0].innerHTML = profileScore.toString()
            $.ajax({
                url:url,
                type:'post',
                data:serializedData,
                success:function(){
                //whatever you wanna do after the form is successfully submitted
                console.log('ajax has submitted form')
                $('.score').show(1000,function(){
                   
                    setTimeout(loadQuestion, 3000)
                })
            }
            })
        })
        
    }
    xhr.send()
}




