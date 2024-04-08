import React, { useState } from 'react';
import { Button } from 'antd';
import { AudioOutlined, StopOutlined } from '@ant-design/icons';
import { ReactMediaRecorder } from "react-media-recorder";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import axios from 'axios';
import './App.css'; // Make sure to import the CSS for styling

function App() {

  const handleRecordClick = () => {
    
    // Add your logic here
  };

  const handleStopClick = () => {
    
    // Add your logic here
  };

  const handleClearHistoryClick = async () => {
    try {
      const response = await axios.get('http://localhost:8000/clear');
      if (response.statusText == 'OK') {
        toast.success('Chat history has been cleared!');
      }
    } catch (error) {
      console.error(error);
    }
  };

  const handleStop = async (blobUrl, blob) => {
    const formData = new FormData()
    formData.append('file', blob, 'myvoice.wav')
    try {
      const response = await axios.post('http://localhost:8000/talk', formData, {
      headers: {
        "Content-Type": "audio/mp3"
      },
      responseType: 'arraybuffer'
    })
    // Get the audio back and play it
    const data = response.data
    const blobMpeg = new Blob([data], { type: 'audio/mpeg' });
    const audio = new Audio();
    audio.src = window.URL.createObjectURL(blobMpeg);
    audio.play();
    } catch (error) {
      console.error(error);
    }
    
  }

  return (
    <ReactMediaRecorder
      audio
      onStop={handleStop}
      render={({ status, startRecording, stopRecording }) => (
        <div className="App">
          <div className="button-container">
            <ToastContainer />
            <Button
              className={`record-button ${status === 'recording' ? 'recording' : ''}`}
              type="primary"
              shape="circle"
              icon={<AudioOutlined />}
              size="large"
              style={{ backgroundColor:'red' , color: 'white', margin: '0 10px' }}
              onClick={startRecording}
            />
            <Button
              className={`stop-button ${status === 'recording' ? 'recording' : ''}`}
              shape="circle"
              icon={<StopOutlined />}
              size="large"
              style={{ backgroundColor: 'white', borderColor: 'red', color: 'red', margin: '0 10px' }}
              onClick={stopRecording}
            />
            <Button
              className='clear-button'
              type="primary"
              shape="round"
              size="large"
              style={{ backgroundColor: 'green', borderColor: 'green', color: 'white', margin: '0 10px' }}
              onClick={handleClearHistoryClick}

            >
              Clear History
            </Button>
          </div>
        </div>
      )}
    />
  );


}

export default App;
