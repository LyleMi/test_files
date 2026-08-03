
fetch('/tutorial/items/'+encodeURIComponent(itemCode)+'?locale=en&expand='+expand,{method:'PUT',headers:{Authorization:'Bearer '+token,'Content-Type':'application/json'},body:JSON.stringify({caption})});
const filter=new URLSearchParams();filter.append('category',category);filter.append('order','recent');
fetch('/tutorial/filter',{method:'POST',body:filter});
const packet=new FormData();packet.append('attachment',attachment);packet.append('purpose','review');
fetch('/tutorial/packages',{method:'POST',body:packet});