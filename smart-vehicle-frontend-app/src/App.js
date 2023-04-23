import logo from './logo3.png';
import Button from 'react-bootstrap/Button';
import './App.css';
import React from 'react';

export async function trainAPI(data) {
  console.log("data: ", data);
  const response = await fetch(`/train`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)
    })
  return await response.json();
}

export async function testAPI(data) {
  console.log("data: ", data);
  const response = await fetch(`/test`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)
    })
  return await response.json();
}

export async function loadModelAPI(data) {
  console.log("data: ", data);
  const response = await fetch(`/train/load`, {
      method: 'GET',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({user: data})
    })
  return await response.json();
}

export async function checkStatusAPI() {
  console.log('here')
  const response = await fetch(`/status`, {
      method: 'GET',
      headers: {'Content-Type': 'application/json'}
    });
    console.log("here2", response);
  return await response.json();
}

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      trained: false,
      trainingProgress: false,
      selectedFile: null
    }
    this.startTraining = this.startTraining.bind(this);
    this.checkStatus = this.checkStatus.bind(this);
    this.test = this.test.bind(this);
  }

  onFileChange = event => {
    console.log("on file change");
    this.setState({ selectedFile: event.target.files[0] });
   
  };

  onFileUpload = () => {
    console.log("------ file upload");
    const formData = new FormData();
    formData.append(
      "myFile",
      this.state.selectedFile,
      this.state.selectedFile.name
    );
    console.log(this.state.selectedFile);
    testAPI(formData);
  };


  startTraining() {
    console.log(this);
    this.setState({trained: true, trainingProgress: true})
    trainAPI({}).then(response => {
      console.log('response: ', JSON.stringify(response));
    });
    console.log("Click");
  
  }

  test() {
    console.log("in test");
    testAPI(this.state.testData);
  }

  checkStatus() {
    // }, 5000);
    // setTimeout(() => { 
    //   console.log("5 secs over !"); 
    checkStatusAPI();
    this.setState({trained: true, trainingProgress: false});

  }

  render() {
    const trained = this.state.trained;
    const trainingProgress = this.state.trainingProgress;
    let p;
    if(!trained) {
      p = <Button variant='primary' onClick={this.startTraining}>Start Training</Button>
    } else if(trained && trainingProgress) {
      p = <div>
            <h3>Training in Progress</h3>
            <p class="lead">This may take some time.</p>
            <Button variant='primary' onClick={this.checkStatus}>Check Status</Button>
          </div>
    } else {
      p = <div>
            <h3>Training Complete. Test Screen</h3>
            <p class="lead">
              Training is complete. Let us test with real world data. 
              <br/>
            </p>
            <br></br>
            <br></br>
            <input type="file" name="file" 
              // value={selectedFile} 
              style={{paddingLeft:'120px'}}
              onChange={this.onFileChange}
            />
            <br></br>
            <br></br>
            {/* <input type="file" onChange={this.onFileChange} />
                <button onClick={this.onFileUpload}> */}

            <Button variant="primary" onClick={this.onFileUpload}> Identify signal </Button>
            <br></br>
            <br></br>
            {/* {this.state.selectedFile &&
              <img alt="preview image" src={URL.createObjectURL(this.state.selectedFile)}/>
            } */}
            <p class="lead">
              Detected {}_____ sign ahead. Accuracy : {}%
            </p>
          </div>
    }

    return (
      <div>
        <br></br>
        <header>
          <nav class="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
            <div class="container-fluid">
              <a class="navbar-brand" href="#">Smart Vehicle Assistance System</a>
              <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
              </button>
            </div>
          </nav>
        </header>
    
        <main class="flex-shrink-0">
          <center>
            <div class="container">
              <h1 class="mt-5">Smart Vehicle Assistance System</h1>
              <p class="lead">Use the Smart Vehicle Assistance System to guide on traffic signals</p>
              {this.state.trained && this.state.selectedFile ?
              <img alt="preview image" src={URL.createObjectURL(this.state.selectedFile)}/> :
              <img src={logo} alt="logo" />
            }
                <br></br>
                <br></br>
                {p}
              <br></br>
              <br></br>
            </div>
          </center>
        </main>
      </div>
    );
  }
  
}

export default App;
