
$( document ).ready(function() {
	$('a').click(function(e) {
		alert ('This link will no longer take you to the destination. Why? Because We prevented the default handler from executing! argument.preventDefault(). Usually e.preventDefault()');
		e.preventDefault();
		$(this).hide('slow');
	});

	$('a').addClass('test');

	var foo = new Array(100);
	alert(foo[0]);
	alert(foo.length);

	var bar = [3];
	alert (bar[0]);
	alert(bar.length);
	bar.push('hi');
	bar.pop();

	jQuery.isFunction(foo);
	jQuery.isPlainObject(foo);
	alert(jQuery.isArray(foo));
	alert(typeof bar === 'string');
	typeof bar === 'integer';
	typeof bar === 'array';
});