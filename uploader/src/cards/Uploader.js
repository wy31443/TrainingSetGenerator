import React,{Component} from 'react';
import { Alert, Uploader, List, Button, Icon, Header, Container, Content  } from 'rsuite';


const styleSpaceBetween = {
  display: 'flex',
  justifyContent: 'space-around',
  alignItems: 'center',
  height: '20px',
  // margin: '10px'
};

export default class VideoUploader extends Component {
  
    constructor(props) {
      super(props);
      this.state = {
        uploadedVideos: [],
        processedVideos: [],
        processing: [],
      };
    }
    onFailedUpload = (response) => {
      Alert.error("Error: " + response.message, 5000);
    }
    onSuccessUpload = (response) => {
      this.getUploaded();
      Alert.success("Success uploaded file", 5000);
    }

    processVideo = (video) => {
      this.setState({processing:[...this.state.processing, video]})
      const axios = require('axios');
      axios.post('/api/v1/process?filename='+video)
        .then(response => {
          this.setState({processing: this.state.processing.filter(function(item) { 
              return item !== video
          })});
          this.setState({processedVideos:[...this.state.processedVideos, video]})
          Alert.success("Successfully processed file " + video, 5000);
        })
        .catch(response =>{
          this.setState({processing: this.state.processing.filter(function(item) { 
              return item !== video
          })});
          Alert.error("Error: " + response.response.data, 5000);
        });  
    }

    renderListButton = (item) => {
      console.log(this.state.processing);
      if(this.state.processing.includes(item)){
        return (
          <Icon icon="spinner" spin />
        )
      }else if(this.state.processedVideos.includes(item)){
        return (
          <Icon icon='check-square-o' size="1x" />
        )
      }else{
        return (
          <Button onClick={()=>this.processVideo(item)}>Process Video</Button>
        )
      }
    }
    renderUploaded = () => {
      if (this.state.uploadedVideos!=null) {
        return <List hover style={{margin: "10px"}}>
                {this.state.uploadedVideos.map((item, index) => (
                  <List.Item key={index} index={index}>
                    <div style={styleSpaceBetween}>
                    {item}
                    { this.renderListButton(item) }
                    </div>
                  </List.Item>
                ))}
              </List>
      }else{
        return <h5>Empty</h5>
      }
    }
    getUploaded = () => {
      const axios = require('axios');
      axios.get('/api/v1/upload')
        .then(response => {
          this.setState({uploadedVideos: response.data})
        })
        .catch(response =>{
          Alert.error("Error: " + response.message, 5000);
        })
        .then(function () {
          // always executed
        });  
    }
    getStatus = () => {
      const axios = require('axios');
      axios.get('/api/v1/process')
        .then(response => {
          this.setState({processedVideos: response.data})
        })
        .catch(response => {
          Alert.error("Error: " + response.message, 5000);
        })
        .then(function () {
          // always executed
        });  
    }
    componentDidMount() {
      this.getUploaded();
      this.getStatus();
    }
    render() {
    
      return (
        <div>
            <Container style={{margin: "10px"}}>
              <Header style={{margin: "10px"}}>
                <h1>
                  Traning Set Generator
                </h1>
              </Header>
              <Content style={{margin: "10px"}}>
                <h3>
                  Uploaded videos
                </h3>
                {this.renderUploaded()}
                <div>
                  <h3>
                    Upload a video file
                  </h3>
                  <Uploader action="api/v1/upload" 
                            accept="*.mp4" 
                            onError={this.onFailedUpload}
                            onSuccess={this.onSuccessUpload}
                            style={{margin: "10px"}}
                            />
                </div>
              </Content>
            </Container>
        </div>
      );
    }
  }
 
