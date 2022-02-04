const button = document.querySelector('#chat-submit');
const submit = document.querySelector('.submit');

function toggleClass() {
	this.classList.toggle('active');
}

function addClass() {
	this.classList.add('finished');
}

button.addEventListener('click', toggleClass);
button.addEventListener('transitionend', toggleClass);
button.addEventListener('transitionend', addClass);