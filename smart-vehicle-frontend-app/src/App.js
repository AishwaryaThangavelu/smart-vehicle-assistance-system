import logo from './logo3.png';
import Button from 'react-bootstrap/Button';
import './App.css';
import React from 'react';
import Spinner from 'react-bootstrap/Spinner';

export async function trainAPI() {
  const response = await fetch(`http://127.0.0.1:5000/test`, {
      method: 'GET',
      headers: {'Content-Type': 'application/json', 
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': "GET",
                'Access-Control-Allow-Headers': "Content-Type"}
    })
  return await response.json();
}

export async function testAPI() {
  // console.log("data: ", data);
  const response = await fetch(`http://127.0.0.1:5000/test`, {
      method: 'GET',
      headers: {'Content-Type': 'application/json','Access-Control-Allow-Origin': '*'}
    })
  return await response.json();
}

class App extends React.Component {
  constructor(props) {
    super();
    this.state = {
      trained: false,
      trainingProgress: false,
      result: [],
      prediction: "",
      score: 0
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
    
    trainAPI().then(response => {
      console.log('response: ', JSON.stringify(response));
      this.setState({trained: true, trainingProgress: false})
      this.setState({result: response})
    });
    console.log("Click");
  }

  test() {
    let _this = this;
    for(let i=0; i<this.state.result.length; i++){
      let image = this.state.result[i];
      setTimeout(function() {
        let img_path = image["img_path"];
        _this.setState({selectedFile: image["img_path"], prediction: image["prediction"], score: image["score"]});
      }, 3000 * i);
    };
  }

  render() {
    const trained = this.state.trained;
    const trainingProgress = this.state.trainingProgress;
    let p;
    if(!trained) {
      p = <Button variant='primary' onClick={this.startTraining}>Train and Test Model-1</Button>
    } else if(trained && trainingProgress) {
      p = <div>
            <h3>Training in Progress</h3><Spinner></Spinner>
            <p class="lead">This may take some time.</p>
          </div>
    } else {
      p = <div>
            <h3>Training Complete. Test Screen</h3>
            <p class="lead">
              Training is complete. Let us test with real world data. 
              <br/>
            </p>
            <Button variant="primary" onClick={this.test}> Test </Button>
            <br></br>
            <br></br> 
            <p class="lead">
              Detected <b>{this.state.prediction}</b> sign ahead. Accuracy : {this.state.score}%
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
              // <img alt="preview image" src={URL.createObjectURL(this.state.selectedFile)}/> :
              <img alt="preview image" src={this.state.selectedFile} key={this.state.selectedFile}/> :
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
