import React from 'react'


class TechnicianForm extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      name: '',
      employee_number: '',
    }
    this.handleSubmit = this.handleSubmit.bind(this)
    this.handleNameChange = this.handleNameChange.bind(this)
    this.handleEmployeeNumberChange = this.handleEmployeeNumberChange.bind(this)
  }
  handleNameChange(event) {
    const value = event.target.value
    this.setState({name: value})
  }
  handleEmployeeNumberChange(event) {
    const value = event.target.value
    this.setState({employee_number: value})
  }
  async handleSubmit(event) {
    event.preventDefault()
    const data = {...this.state}
    console.log("::::::::", data)

    const technicianUrl = 'http://localhost:8080/api/technicians/'
    const fetchConfig = {
      method: "post",
      body: JSON.stringify(data),
      headers: {
        'Content-Type': 'application/json'
      }
    }
    const response = await fetch(technicianUrl, fetchConfig)
    if (response.ok) {
      const newTechnician = await response.json()
      console.log(newTechnician)

      const cleared = {
        name: '',
        employee_number: '',
      }
      this.setState(cleared)
    }
    alert('A form was submitted: ' + this.state.name + ' // ' + this.state.employee_number)

  }

  render () {
    return (
    <div className="container">
      <div className="row">
        <div className="offset-3 col-6">
          <div className="shadow p-4 mt-4">
            <h1>Add a new technician</h1>
            <form onSubmit={this.handleSubmit} id="create-technician-form">
              <div className="form-floating mb-3">
                <input onChange={this.handleNameChange} value={this.state.name} placeholder="Name" required type="text" name="name" id="name" className="form-control"/>
                <label htmlFor="name">Name</label>
              </div>
              <div className="form-floating mb-3">
                <input onChange={this.handleEmployeeNumberChange}  value={this.state.employee_number} placeholder="Employee number" required type="number" name="employee_number" id="employee_number" className="form-control"/>
                <label htmlFor="employee_number">Employee number</label>
              </div>
              <button className="btn btn-primary">Create</button>
            </form>
          </div>
        </div>
      </div>
    </div>
    )
  }
}

export default TechnicianForm
