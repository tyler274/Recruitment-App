$(document).ready(function () {
$(".nmt").each(function() {
var nmtTable = $(this);
var nmtHeadRow = nmtTable.find("thead tr");
nmtTable.find("tbody tr").each(function () {
var curRow = $(this);
for (var i = 0; i < curRow.find("td").length; i++) {
var rowSelector = "td:eq(" + i + ")";
var headSelector = "th:eq(" + i + ")";
curRow.find(rowSelector).attr('data-title', nmtHeadRow.find(headSelector).html());
}
});

});
});
