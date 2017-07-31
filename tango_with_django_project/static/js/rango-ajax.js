$('#likes').click(function(){
		var catid = 0;
		catid = $(this).attr('data-catid');

		$.get('/rango/like_category/',{'category_id':catid},function(data){
			$('#like_count').html(data);
			$('#likes').hide();
		});
	});
$('#suggestion').keyup(function(){
	let query;
	query = $(this).val();
	console.log(query);
	$.get('/rango/suggest_category/',{'suggestion':query},
	function(data){
		$('#cats').html(data);
	});
});
$('.rango-add').click(function(){
	const context_dict ={
			'catid' : $(this).attr('data-catid'),
			'url' : $(this).attr('data-url'),
			'title':$(this).attr('data-title')
		}
	console.log(context_dict);
	const me = $(this);
	$.get('/rango/quick_add/',context_dict,function(data){
		$('#pages').html(data);
		me.hide();
	});
});