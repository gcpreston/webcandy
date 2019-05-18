import React from "react";
import FadecandyForm from "./components/FadecandyForm";
import { Col, Container, Row } from "react-bootstrap";

export default class App extends React.Component {
  render() {
    return (
      <Container>
        <Row>
          <Col className="text-center">
            <div className="d-inline-block w-75 p-2" id="intro-wrapper">
              <h1>Webcandy!</h1>
              <div className="text-left" id="intro-paragraph-wrapper">
                {/*
                    TODO[INFO]: Add information on how to use the web app 
                    along with personal fadecandy server 
                */}
                <p className="lead">
                  This should be turned into an explanation of the web app and
                  how to use it along with your fadecandy.
                </p>
                <p className="lead">
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
                  do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                  Ut enim ad minim veniam, quis nostrud exercitation ullamco
                  laboris nisi ut aliquip ex ea commodo consequat. Duis aute
                  irure dolor in reprehenderit in voluptate velit esse cillum
                  dolore eu fugiat nulla pariatur. Excepteur sint occaecat
                  cupidatat non proident, sunt in culpa qui officia deserunt
                  mollit anim id est laborum.
                </p>
              </div>
            </div>
            <div className="d-inline-block w-75" id="form-wrapper">
              <FadecandyForm />
            </div>
          </Col>
        </Row>
      </Container>
    );
  }
}
