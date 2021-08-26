import React,{Component} from 'react';
import { Sidebar, Header, Container, Content, List, Alert, Button } from 'rsuite';

const styleSpaceBetween = {
  display: 'flex',
  justifyContent: 'space-around',
  alignItems: 'center',
  height: '20px',
  // margin: '10px'
};
export default class Labeler extends Component {
    constructor(props) {
      super(props);
      this.state = {
        activeImg: null,
        activeLabel: null,
        labels: []
      };
    }

    renderLabels = () => {
      return (
          this.state.labels.map((item, index) => (
            <List.Item key={item} index={index}>
              <div style={styleSpaceBetween}>
                {item}<Button key={"button-"+item} onClick={e => this.labelClicked(e)}>+</Button>
              </div>
            </List.Item>
          ))
        )
    }
    labelClicked = (e) => {
      console.log(e.target.key);
      // this.setState({activeLabel: e})
    }
    getLabels = () => {
      
      const axios = require('axios');
      axios.get('/api/v1/labels')
        .then(response => {
          this.setState({labels: response.data})
        })
        .catch(response => {
          Alert.error("Error: " + response.message, 5000);
        });  
    }
    componentDidMount() {
      this.getLabels();
    }
    render() {
    
      return (
        <>
            <Container>
            <Sidebar style={{margin: "10px"}}>
              <List hover>
                {this.renderLabels()}
              </List>
            </Sidebar>
            <Container style={{margin: "10px"}}>
              <Header style={{margin: "10px"}}>
                <h1>
                  Labeling Image
                </h1>
              </Header>
              <Content style={{margin: "10px"}}>Content</Content>
            </Container>
          </Container>
            
            <div>
                
            </div>
        </>
      );
    }
  }
 
