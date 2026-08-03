
const workshopRoot=settings.serviceRoot;
const boardUrl=`${workshopRoot}${registry.paths.board}?page=${page}`;
if(settings.features.boards)fetch(boardUrl);
const cardPath=registry.paths.card.replace(':cardRef',encodeURIComponent(cardRef));
if(settings.features.editCards)fetch(workshopRoot+cardPath,{method:'PUT',headers:{'X-Audit-Token':auditToken},body:JSON.stringify({label})});
if(settings.features.archive)fetch(workshopRoot+registry.paths.archive);