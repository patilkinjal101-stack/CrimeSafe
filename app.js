function chart(id,type,labels,data,label){
 new Chart(document.getElementById(id),{type:type,data:{labels:labels,datasets:[{label:label,data:data,borderWidth:2}]},
 options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:type!=="bar"}}}});
}
