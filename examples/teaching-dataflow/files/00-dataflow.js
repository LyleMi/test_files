
const root='/lab/v2';
const resource=`${root}/tickets/${encodeURIComponent(ticketKey)}`;
const target=`${resource}?expand=${expand}&fixed=summary`;
const commonHeaders={'X-Academy-Client':'dataflow-lesson'};
function request(url,options={}){
  const merged={method:'GET',...options};
  merged.headers={...commonHeaders,...options.headers};
  return fetch(url,merged);
}
const options={method:'PATCH'};
options.headers={'X-Flow-Trace':trace,'Content-Type':'application/json'};
options.body=JSON.stringify({title,closed});
request(target,options);
const queueTarget=root+'/queues?region='+region;
request(queueTarget);