import React, {Component} from 'react';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';
import BaseTablePage from './BaseTablePage';
import IconButton from '@material-ui/core/IconButton';
import AddCircle from '@material-ui/icons/AddCircle';
import Edit from '@material-ui/icons/Edit';
import DeviceHub from '@material-ui/icons/DeviceHub';
import { Link } from 'react-router-dom'
import axios from 'axios'


class CampaignsPage extends Component {

  state = {
    rows: [],
    columns: [
      {'attrName': 'prepid', 'displayName': 'PrepID', 'visible': 1},
      {'attrName': '_actions', 'displayName': 'Actions', 'visible': 1},
      {'attrName': 'energy', 'displayName': 'Energy', 'visible': 1},
      {'attrName': 'is_root', 'displayName': 'Root', 'visible': 1},
      {'attrName': 'cmssw_release', 'displayName': 'CMSSW release', 'visible': 0},
      {'attrName': 'events_per_lumi', 'displayName': 'Events per lumi', 'visible': 0},
      {'attrName': 'generators', 'displayName': 'Generators', 'visible': 0},
      {'attrName': 'history', 'displayName': 'History', 'visible': 1},
      {'attrName': 'input_dataset', 'displayName': 'Input dataset', 'visible': 0},
      {'attrName': 'memory', 'displayName': 'Memory', 'visible': 1},
      {'attrName': 'no_output', 'displayName': 'No output', 'visible': 0},
      {'attrName': 'notes', 'displayName': 'Notes', 'visible': 1},
      {'attrName': 'on_hold', 'displayName': 'On hold', 'visible': 0},
      {'attrName': 'pileup_dataset_name', 'displayName': 'Pileup dataset name', 'visible': 0},
      {'attrName': 'sequences', 'displayName': 'Sequences', 'visible': 0},
      {'attrName': 'status', 'displayName': 'Status', 'visible': 0},
      {'attrName': 'type', 'displayName': 'Type', 'visible': 0}
    ]
  }

  async createRequest(campaignPrepid) {
    console.log('Create request for ' + campaignPrepid)
    const {data} = await axios.put('http://instance1.cern.ch/api/requests/create', {'campaign': campaignPrepid, 'pwg': 'DBG' })
    console.log(data.results)
  }

  render() {
    return (
      <div>
        <BaseTablePage changeColumns={({columns}) => this.setState({columns})} dbName='campaigns' columns={this.state.columns} onDataFetched={({rows}) => this.setState({rows})}>
          <TableBody>
            {this.state.rows.map(row => {
              return (
                <TableRow key={row._id}>
                  {this.state.columns.filter(function (attr) {return attr.visible === 1}).map(attr => {
                    var cellValue = undefined;
                    cellValue = ''
                    if (attr.attrName === '_actions') {
                      cellValue = <div>
                                    <IconButton title={"Edit " + row.prepid}><Edit /></IconButton>
                                    <IconButton onClick={() => this.createRequest(row.prepid)} title={"Create request for " + row.prepid}><AddCircle /></IconButton>
                                    <IconButton component={Link} to={"/requests?member_of_campaign=" + row.prepid} title={"Requests from " + row.prepid}><DeviceHub /></IconButton>
                                  </div>
                    } else if (attr.attrName === 'history') {
                      cellValue = <ul>{row[attr.attrName].map(entry => {return <li key={entry.time}>{entry.username}&nbsp;at&nbsp;{entry.time}&nbsp;{entry.action}&nbsp;{entry.value}</li>})}</ul>
                    } else if (attr.attrName === 'generators') {
                      cellValue = <ul>{row[attr.attrName].map(generator => {return <li key={generator}>{generator}</li>})}</ul>
                    } else if (attr.attrName === 'events_per_lumi') {
                      cellValue = <ul>{Object.entries(row[attr.attrName]).map( ([key, value]) => <li>{key}:&nbsp;{value}</li> )}</ul>
                    } else if (attr.attrName === 'is_root' || attr.attrName === 'on_hold') {
                      cellValue = row[attr.attrName] === 1 ? 'Yes' : 'No'
                    } else if (row[attr.attrName] !== undefined) {
                      cellValue = row[attr.attrName].toString()
                    }
                    return (
                      <TableCell key={attr.attrName}>{cellValue}</TableCell>
                    )
                  })}
                </TableRow>
              );
            })}
          </TableBody>
        </BaseTablePage>
      </div>
    )
  }
}

export default CampaignsPage;