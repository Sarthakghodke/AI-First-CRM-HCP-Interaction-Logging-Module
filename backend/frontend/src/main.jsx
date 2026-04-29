import React from 'react'
import { createRoot } from 'react-dom/client'
import { Provider } from 'react-redux'
import { configureStore, createSlice } from '@reduxjs/toolkit'

const interactionSlice = createSlice({
  name: 'interaction',
  initialState: { hcp_name: '', channel: 'In-person', summary: '', mode: 'form', chat: '', response: '' },
  reducers: {
    setField: (state, action) => { state[action.payload.key] = action.payload.value },
  },
})

const store = configureStore({ reducer: { interaction: interactionSlice.reducer } })
const { setField } = interactionSlice.actions

function App() {
  const s = store.getState().interaction
  const submitForm = async () => {
    await fetch('http://localhost:8000/interactions', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ hcp_name: s.hcp_name, channel: s.channel, summary: s.summary }) })
    alert('Interaction logged via form')
  }
  const sendChat = async () => {
    const res = await fetch('http://localhost:8000/agent/chat', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ message: s.chat }) })
    const json = await res.json()
    store.dispatch(setField({ key: 'response', value: `${json.tool_used}: ${json.response}` }))
  }
  store.subscribe(() => createRoot(document.getElementById('root')).render(<Provider store={store}><App /></Provider>))
  return <div style={{fontFamily:'Inter, sans-serif',maxWidth:800,margin:'30px auto'}}>
    <h1>Log Interaction Screen</h1>
    <button onClick={()=>store.dispatch(setField({key:'mode',value:'form'}))}>Form Mode</button>
    <button onClick={()=>store.dispatch(setField({key:'mode',value:'chat'}))} style={{marginLeft:8}}>Chat Mode</button>
    {s.mode==='form' ? <div>
      <input placeholder='HCP Name' onChange={e=>store.dispatch(setField({key:'hcp_name',value:e.target.value}))}/><br/>
      <input placeholder='Channel' onChange={e=>store.dispatch(setField({key:'channel',value:e.target.value}))}/><br/>
      <textarea placeholder='Summary' onChange={e=>store.dispatch(setField({key:'summary',value:e.target.value}))}/><br/>
      <button onClick={submitForm}>Log Interaction</button>
    </div> : <div>
      <textarea placeholder='Type interaction notes or command' onChange={e=>store.dispatch(setField({key:'chat',value:e.target.value}))}/><br/>
      <button onClick={sendChat}>Send</button>
      <pre>{s.response}</pre>
    </div>}
  </div>
}

createRoot(document.getElementById('root')).render(<Provider store={store}><App /></Provider>)