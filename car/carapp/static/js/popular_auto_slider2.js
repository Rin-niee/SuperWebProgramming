let panel = document.querySelector('.popular_auto');
let swipper = document.querySelector('.swipper');
console.log(panel);
let offset = 20; // Начальный сдвиг элементов

function move(item, pos){
	let translateWidth = item.offsetWidth+16;
	console.log(translateWidth);
	offset += pos*(translateWidth+30);
	console.log(offset);
	swipper.style.transform = `translateX(${offset}px)`;
}

panel.addEventListener('click',(event)=>
{
	let parent = event.target.parentNode;
	console.log(parent.id);
	let objects = document.getElementsByClassName('popular_auto_item');
	console.log(objects);
	let index_g = 0;
	if(event.target.classList.contains('nav_right'))
	{
		for (var i = 0; i < objects.length; i++) {
		    element = objects.item(i);
	    	if (element.classList.contains('item_big') && element.parentNode.id == parent.id){ 
		    	index_g = i+1;
		    	element_next = objects.item(index_g);
		    	move(element_next, -1)
		    	element.classList.remove('item_big');
			}
		}
		element_next.classList.add('item_big');
	}
	if(event.target.classList.contains('nav_left'))
	{
		for (var i = 0; i < objects.length; i++) {
		    element = objects.item(i);
	    	if (element.classList.contains('item_big') && element.parentNode.id == parent.id){ 
		    	index_g = i-1;
		    	element_next = objects.item(index_g);
		    	move(element_next, 1)
		    	element.classList.remove('item_big');
			}
		}
		element_next.classList.add('item_big');
	}
});