class ClickButton extends React.Component {

  state = {
    wasClicked : false
  }

  handleClick() { 
    this.setState(
      {
        wasClicked : true
      }
    )
  }

  render() {
    let buttonText;

    if (this.state.wasClicked){
      buttonText = "Button is clicked!"

    }
    else {
      buttonText = "Click me"
    }

    return React.createElement(
      "button", 
      {
        className : "mt-2 btn btn-primary",
        onClick : () => {
          this.handleClick()
        }

      },
      buttonText
    )
  }

}

const domContainer = document.getElementById("react_root")

ReactDOM.render(
  React.createElement(ClickButton),
  domContainer
)