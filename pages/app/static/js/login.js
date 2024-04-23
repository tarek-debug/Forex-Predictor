const mode = 'login';

class LoginComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      mode: this.props.mode };

  }
  toggleMode() {
    var newMode = this.state.mode === 'login' ? 'signup' : 'login';
    this.setState({ mode: newMode });
  }
  render() {
    return /*#__PURE__*/(
      React.createElement("div", null, /*#__PURE__*/
      React.createElement("div", { className: `form-block-wrapper form-block-wrapper--is-${this.state.mode}` }), /*#__PURE__*/
      React.createElement("section", { className: `form-block form-block--is-${this.state.mode}` }, /*#__PURE__*/
      React.createElement("header", { className: "form-block__header" }, /*#__PURE__*/
      React.createElement("h1", null, this.state.mode === 'login' ? 'Welcome back!' : 'Sign up'), /*#__PURE__*/
      React.createElement("div", { className: "form-block__toggle-block" }, /*#__PURE__*/
      React.createElement("span", null, this.state.mode === 'login' ? 'Don\'t' : 'Already', " have an account? Click here \u2192"), /*#__PURE__*/
      React.createElement("input", { id: "form-toggler", type: "checkbox", onClick: this.toggleMode.bind(this) }), /*#__PURE__*/
      React.createElement("label", { htmlFor: "form-toggler" }))), /*#__PURE__*/


      React.createElement(LoginForm, { mode: this.state.mode, onSubmit: this.props.onSubmit }))));



  }}


class LoginForm extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    return /*#__PURE__*/(
      React.createElement("form", { onSubmit: this.props.onSubmit }, /*#__PURE__*/
      React.createElement("div", { className: "form-block__input-wrapper" }, /*#__PURE__*/
      React.createElement("div", { className: "form-group form-group--login" }, /*#__PURE__*/
      React.createElement(Input, { type: "text", id: "username", label: "user name", disabled: this.props.mode === 'signup' }), /*#__PURE__*/
      React.createElement(Input, { type: "password", id: "password", label: "password", disabled: this.props.mode === 'signup' })), /*#__PURE__*/

      React.createElement("div", { className: "form-group form-group--signup" }, /*#__PURE__*/
      React.createElement(Input, { type: "text", id: "fullname", label: "full name", disabled: this.props.mode === 'login' }), /*#__PURE__*/
      React.createElement(Input, { type: "email", id: "email", label: "email", disabled: this.props.mode === 'login' }), /*#__PURE__*/
      React.createElement(Input, { type: "password", id: "createpassword", label: "password", disabled: this.props.mode === 'login' }), /*#__PURE__*/
      React.createElement(Input, { type: "password", id: "repeatpassword", label: "repeat password", disabled: this.props.mode === 'login' }))), /*#__PURE__*/


      React.createElement("button", { className: "button button--primary full-width", type: "submit" }, this.props.mode === 'login' ? 'Log In' : 'Sign Up')));


  }}


const Input = ({ id, type, label, disabled }) => /*#__PURE__*/
React.createElement("input", { className: "form-group__input", type: type, id: id, placeholder: label, disabled: disabled });


const App = () => /*#__PURE__*/
React.createElement("div", { className: `app app--is-${mode}` }, /*#__PURE__*/
React.createElement(LoginComponent, {
  mode: mode,
  onSubmit:
  function () {
    console.log('submit');
  } }));





ReactDOM.render( /*#__PURE__*/React.createElement(App, null), document.getElementById("app"));