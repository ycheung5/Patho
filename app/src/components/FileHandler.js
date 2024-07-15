import React, { useState } from 'react';

const FileHandler = () => {
    const [file, setFile] = useState(null);
    const [sequence, setSequence] = useState('');
    const [inputMethod, setInputMethod] = useState('file');

    const handleFileChange = (event) => {
        const file = event.target.files ? event.target.files[0] : null;
        setFile(file);
    };

    const handleInputMethod = (event) => {
        const preference = event.target.value;
        setInputMethod(preference);
    }

    const handleSequence = (event) => {
        const sequ = event.target.value;
        setSequence(sequ);
    }

    const processFile = async () => {
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('http://localhost:8000/upload_file', {
                method: 'POST',
                body: formData,
            });

            console.log(response);
            if (!response.ok) {
                alert('Failed to fetch file!');
                throw new Error('Network response was not ok');
            }

            // Assuming the server responds with a Blob (file data)
            const blob = await response.blob();
            const downloadUrl = window.URL.createObjectURL(blob);

            // Create a link and trigger download
            const a = document.createElement("a");
            a.href = downloadUrl;
            console.log(a);
            document.body.appendChild(a);
            a.click();

            // Clean up by revoking the Blob URL and removing the anchor element
            window.URL.revokeObjectURL(downloadUrl);
            document.body.removeChild(a);

        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }
    };

    const processSequence = async () => {
        if (!sequence) return;

        try {
            const response = await fetch(`http://localhost:8000/upload_sequence/${sequence}`, {
                method: 'POST',
            });

            console.log(response);
            if (!response.ok) {
                alert('Please insert a valid genome which only contains "ATCG"');
                throw new Error('Network response was not ok');
            }

            // Assuming the server responds with a Blob (file data)
            const blob = await response.blob();
            const downloadUrl = window.URL.createObjectURL(blob);

            // Create a link and trigger download
            const a = document.createElement("a");
            a.href = downloadUrl;
            console.log(a);
            document.body.appendChild(a);
            a.click();

            // Clean up by revoking the Blob URL and removing the anchor element
            window.URL.revokeObjectURL(downloadUrl);
            document.body.removeChild(a);

        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }

    };

    return (
        <div style={{padding: '20px', textAlign: 'center' }}>
            <form style={{margin: '15px'}}>
                <fieldset>
                    <legend style={{padding: '5px'}}>Please select your preferred input method:</legend>
                    <div onChange={handleInputMethod} style={{padding: '5px'}}>
                        <input type="radio" id="contactChoice1" name="contact" value="file" checked={inputMethod === 'file'}/>
                        <label htmlFor="contactChoice1" style={{marginRight: '5px'}}>File</label>
                        <input type="radio" id="contactChoice2" name="contact" value="sequence" checked={inputMethod === 'sequence'}/>
                        <label htmlFor="contactChoice2" style={{marginLeft: '5px'}}>Sequence</label>
                    </div>
                </fieldset>
            </form>
            {
                inputMethod === 'file' ?
                    <input type="file" onChange={handleFileChange} style={{display: 'block', margin: '20px auto'}}/>
                    :
                    <div style={{display: 'flex'}}>
                        <label htmlFor={'seq'} style={{marginRight: '5px'}}>Sequence: </label>
                        <textarea id={'seq'} style={{resize: 'none'}} rows={10} cols={80} onChange={handleSequence}/>
                    </div>
            }
            {
                inputMethod === 'file' ?
                    <button onClick={processFile} disabled={!file} style={{
                        padding: '10px 20px',
                        cursor: 'pointer',
                        backgroundColor: '#007BFF',
                        color: 'white',
                        border: 'none',
                        borderRadius: '5px'
                    }}>
                        Process File
                    </button>
                    :
                    <button onClick={processSequence} disabled={!sequence} style={{
                        padding: '10px 20px',
                        margin: '10px',
                        cursor: 'pointer',
                        backgroundColor: '#007BFF',
                        color: 'white',
                        border: 'none',
                        borderRadius: '5px'
                    }}>
                        Process Sequence
                    </button>

            }
        </div>
    );
};

export default FileHandler;