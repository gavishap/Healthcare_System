const configured=(import.meta as unknown as {env:Record<string,string>}).env.VITE_API_BASE_URL || ''
export const API=configured.replace(/\/$/,'')
let token=''
export function setAccessToken(value:string){token=value}
export async function request<T>(path:string,init:RequestInit={}):Promise<T>{
  const response=await fetch(API+path,{...init,headers:{...(init.body?{'Content-Type':'application/json'}:{}),...(token?{Authorization:`Bearer ${token}`} : {}),...init.headers}})
  if(!response.ok){
    let detail='The service could not complete this request.'
    try {const data=await response.json(); detail=typeof data.detail==='string'?data.detail:JSON.stringify(data.detail)} catch { /* never expose arbitrary upstream bodies */ }
    throw new Error(response.status===401?'ACCESS_REQUIRED':detail)
  }
  return response.json() as Promise<T>
}
export async function downloadReport(id:string,format:'markdown'|'json'){
  const response=await fetch(`${API}/api/research-runs/${id}/export?format=${format}`,{headers:token?{Authorization:`Bearer ${token}`}:{}})
  if(!response.ok)throw new Error('The export is not available yet.')
  const blob=await response.blob();const url=URL.createObjectURL(blob)
  const link=document.createElement('a');link.href=url;link.download=`evidence-briefing-${id.slice(0,8)}.${format==='json'?'json':'md'}`;link.click()
  setTimeout(()=>URL.revokeObjectURL(url),1000)
}
