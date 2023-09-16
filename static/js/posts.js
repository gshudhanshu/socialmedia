// I wrote this code

// Add event listener to all the comment forms
document.querySelectorAll('.comment-form').forEach(formContainer => {
    formContainer.addEventListener('submit', function (e) {
        // Prevent the default form submission
        e.preventDefault();

        const post_id = this.getAttribute('data-post-id');
        // Get the comment text
        let commentInput = this.querySelector("input");
        let comment_text = commentInput.value;
        console.log('post_Id: ' + post_id, 'comment_text: ' + comment_text);
        axiosPostRequest(post_id, comment_text, commentInput, formContainer)
    })
});

// function to make axios POST request to create a new comment
function axiosPostRequest(post_Id, comment_text, commentInput, formContainer) {
    axios.post('/comment/create', {post: post_Id, content: comment_text}, {
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        }
    })
        .then(response => {
            console.log('New Comment:', response.data);

            // Append the new comment to the comments container at the beginning
            const commentsContainer = formContainer.parentElement.querySelector('.comments-container');
            const newCommentHTML = `
                    <div class="flex items-center space-x-2">
                        <img src="${response.data.user_profile.profile_image}" alt=""
                            class="object-cover object-center w-4 h-4 rounded-full shadow-sm dark:bg-gray-500 dark:border-gray-700">
                        <div class="-space-y-1">
                            <div class="-space-y-1">
                                <span class="font-semibold leadi">
                                    ${response.data.user_details.username}
                                </span>
                                <span class="inline-block leadi dark:text-gray-400">
                                    ${response.data.content}
                                </span>
                            </div>
                        </div>
                    </div>
                `;
            commentsContainer.insertAdjacentHTML('afterbegin', newCommentHTML);
            formContainer.parentElement.parentElement.querySelector('.num-comments').innerHTML = response.data.num_comments + ' users'

            // Clear the input field value
            commentInput.value = '';
        })
        .catch(error => {
            console.error('Error creating comment:', error);
        });
}

// focus the input field when the user clicks on the comment button
function focusInput(button) {
    button.parentElement.parentElement.parentElement.querySelector('.comment-form').querySelector('input').focus();
}

// Like or Unlike a post
function likePost(button) {
    const post_id = button.getAttribute('data-post-id');
    axios.post(`/like/${post_id}`, {post: post_id}, {
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        }
    })
        // On successful response update the button classes and the number of likes
        .then(response => {
            console.log(response.data);
            if (response.data.liked) {
                button.querySelector('svg').classList.add('text-red-500');
                button.querySelector('svg').classList.add('fill-current');
            } else {
                button.querySelector('svg').classList.remove('text-red-500');
                button.querySelector('svg').classList.remove('fill-current');
            }
            button.parentElement.parentElement.parentElement.querySelector('.num-likes').innerHTML = response.data.num_likes + ' users';
        }).catch(error => {
        console.error('Error liking post:', error);
    });
}

// end of code I wrote