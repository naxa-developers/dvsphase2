// Basic DataTable
$(function(){
	$('.program-table').DataTable({
		language: { search: '', searchPlaceholder: "Search..." },
		"scrollX": true,
		"scrollCollapse": true,
		'iDisplayLength': 18,
		"ordering": true,
		"lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
		dom: 'Bfrtip',
        buttons: [
            'excelHtml5',
            'csvHtml5',
        ]
		
	});
});
