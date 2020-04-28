import React from 'react';
import '../BoxStyle.css'

class Main extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      imageURL: '',
    };

    this.handleUploadImage = this.handleUploadImage.bind(this);
  }

  handleUploadImage(ev) {
    ev.preventDefault();

    const data = new FormData();
    console.log("this.uploadInput.files[0]", this.uploadInput.files[0])
    data.append('file', this.uploadInput.files[0]);
    // data.append('filename', this.fileName.value);

    fetch('http://127.0.0.1:4376/file-upload', {
      method: 'POST',
      // headers: { 'Content-Type': 'multipart/form-data',},
      body: data,
     
    }).then(response => response.blob())
    .then(blob => {
      var url = window.URL.createObjectURL(blob);
      var a = document.createElement('a');
      a.href = url;
      a.download = "result";
      document.body.appendChild(a); // we need to append the element to the dom -> otherwise it will not work in firefox
      a.click();
      a.remove();  //afterwards we remove the element again 
  }
)
    .catch((error) => {
      console.error('Error:', error);
    });
    
    // .then((response => {
    //   console.log("Result: ",response.json())
    // })
      
    //   // response.json().then((body) => {
    //   //   alert('dddddddd')
    //   //   this.setState({ imageURL: `http://127.0.0.1:4376/file-upload${body.file}` });
    //   // });
    // );
  // }
  }

  render() {
    return (
      <form  onSubmit={this.handleUploadImage}>
        <div className="form">
          <div>
          <input ref={(ref) => { this.uploadInput = ref; }} type="file" />
          </div>
        {/* <div>
          <input ref={(ref) => { this.fileName = ref; }} type="text" placeholder="Enter the desired name of file" />
        </div> */}
        {/* <img className="img" src={require('../doctor.png')} alt="img" /> */}
        <br />
        <br />
        <br />


        <button className="button">Diagnose</button>

        </div>
      </form>
    );
  }
}

export default Main;