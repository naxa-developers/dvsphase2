// Basic DataTable
$(function(){

	$('.program-table').DataTable({
		language: { search: '', searchPlaceholder: "Search..." },
		"scrollX": true,
		"scrollCollapse": true,
		'iDisplayLength': 100,
		"ordering": true,
		"lengthMenu": [[100, 200, 300, -1], [100, 200, 300, "All"]],
		dom: 'lBfrtip',
        buttons: [
            'excelHtml5',
            'csvHtml5',
        ]
		
	});

	$('.five-table').DataTable({
		language: { search: '', searchPlaceholder: "Search..." },
		"scrollX": true,
		"scrollCollapse": true,
//		'iDisplayLength': 100,
		"ordering": true,
		"bInfo" : false,
		"paging": false,
//		"lengthMenu": [[100, 200, 300, -1], [100, 200, 300, "All"]],
		dom: 'lBfrtip',
        buttons: [
            'excelHtml5',
            'csvHtml5',
        ]

	});


});
