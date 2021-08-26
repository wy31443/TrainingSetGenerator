import './App.css';
import React from 'react';
import VideoUploader from './cards/Uploader';
import Labeler from './cards/Labeler';
import 'rsuite/dist/styles/rsuite-default.css';
import { Navbar, Nav, Icon } from 'rsuite';

const NavBarInstance = ({ onSelect, activeKey, ...props }) => {
  return (
    <Navbar {...props}>
      <Navbar.Header>
        <a href="#" className="navbar-brand logo">
          {/* RSUITE */}
        </a>
      </Navbar.Header>
      <Navbar.Body>
        <Nav onSelect={onSelect} activeKey={activeKey}>
          <Nav.Item eventKey="1" icon={<Icon icon="home" />}>
            Home
          </Nav.Item>
          <Nav.Item eventKey="upload">Upload</Nav.Item>
          <Nav.Item eventKey="label">Label</Nav.Item>
        </Nav>
        <Nav pullRight>
          <Nav.Item icon={<Icon icon="cog" />}>Settings</Nav.Item>
        </Nav>
      </Navbar.Body>
    </Navbar>
  );
};

class App extends React.Component {
  constructor(props) {
    super(props);
    this.handleSelect = this.handleSelect.bind(this);
    this.state = {
      activeKey: null
    };
  }
  handleSelect(eventKey) {
    this.setState({
      activeKey: eventKey
    });
  }
  renderPage() {
    switch(this.state.activeKey) {
      case "upload":
        return <VideoUploader />
      case "label":
        return <Labeler />
      default:
        return (
          <h3 style={{margin: "10px"}}>
            This is a project used to generate training set of yolo, it takes the video and find the most UNBLURRY image of a second among all the frames in that second. 
          </h3>
        )
    }
  }
  render() {
    const { activeKey } = this.state;
    return (
      <>
        <NavBarInstance appearance="inverse" activeKey={activeKey} onSelect={this.handleSelect} />
        { this.renderPage()}
      </>
    );
  }
}

export default App;
