function nospaces(name) {
	form  = document.getElementById("form")
	t = form.get(name)
	if (t.value.match(/\s/g)) t.value = t.value.replace(' ', '');
}
$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
});

var options = [];
$('.dropdown-menu.check-form label').on('click', function(event) {
	var $target = $(event.currentTarget),
		val = $target.attr('data-value'),
		$inp = $target.find('input'),
		label = $target.find('label').prevObject[0],
		idx;
	console.log(label);
	if ((idx = options.indexOf(val)) > -1) {
		options.splice(idx, 1);
		label.classList.add("deselected");
		label.classList.remove("selected");
		setTimeout(function() {
			$inp.prop('checked', false);
		}, 0);
	} else {
		options.push(val);
		label.classList.add("selected");
		label.classList.remove("deselected");
		setTimeout(function() {
			$inp.prop('checked', true);
		}, 0);
	}
	$(event.target).blur();
	console.log(options);
	return false;
});
