import React,{Component} from 'react';
import { Sidebar, Header, Container, Content, List, Alert, Button, Icon } from 'rsuite';
import { Stage, Layer, Image } from 'react-konva';
import useImage from 'use-image';
import axios from 'axios';

const styleSpaceBetween = {
  display: 'flex',
  justifyContent: 'space-around',
  alignItems: 'center',
  height: '20px',
};
const LabelImage = (src) => {
  const [image] = useImage(src);
  return <Image image={image} />;
};
export default class Labeler extends Component {
    constructor(props) {
      super(props);
      this.state = {
        activeImg: undefined,
        folder: undefined,
        frame: undefined,
        activeLabel: undefined,
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
    }
    getLabels = () => {
      axios.get('/api/v1/labels')
        .then(response => {
          this.setState({labels: response.data})
        })
        .catch(response => {
          Alert.error("Error: " + response.message, 5000);
        });  
    }
    renderImage = () => {
      <LabelImage src={this.state.activeImg}/>
    }
    nextImage = () => {
      axios.get('/api/v1/get_next')
      .then(response => {
        console.log(response.data);
        this.setState({activeImg: response.data})
      })
      .catch(response => {
        Alert.error("Error: " + response.message, 5000);
      });  
    }
    componentDidMount() {
      this.getLabels();
      this.nextImage();
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
              <Header>
                <h1>
                  Labeling Image
                  <Button onClick={() => {this.nextImage()}}><Icon icon="page-next"></Icon></Button>
                </h1>
                
              </Header>
              <Content style={{margin: "10px"}}>
                <Stage width={window.innerWidth} height={window.innerHeight}>
                  <Layer>
                    {this.renderImage}
                  </Layer>
                </Stage>
              </Content>
            </Container>
          </Container>
            
            <div>
                
            </div>
        </>
      );
    }
  }
 
