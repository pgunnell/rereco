import React, {Component} from 'react';
import PropTypes from 'prop-types';
import axios from 'axios'
import Table from '@material-ui/core/Table';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import queryString from 'query-string'
import TableFooter from '@material-ui/core/TableFooter';
import TablePagination from '@material-ui/core/TablePagination';
import Paper from '@material-ui/core/Paper';
import Checkbox from '@material-ui/core/Checkbox';
import FormControlLabel from '@material-ui/core/FormControlLabel';



class CampaignsPage extends Component {
    
  constructor (props) {
    super(props)
    this.state = {
      rows: [],
      totalRows: 0,
      columns: props.columns,
      page: 0,
      limit: 20
    }
  }

  columnsToBinary(columns) {
    var shown = 0;
    columns.slice().reverse().forEach(entry => {
        shown = shown << 1;
        if (entry.visible) {
            shown = shown | 1;
        }
    });
    return shown;
  }

  binaryToColumns(shown) {
    var shownCopy = shown;
    var columns = [...this.state.columns]
    columns.forEach(entry => {
      entry.visible = (shownCopy & 1);
      shownCopy = shownCopy >> 1;
    });
    return columns
  }

  componentDidMount() {
    var newState = {}
    const query = queryString.parse(this.context.router.route.location.search)
    if (query.shown === undefined) { 
      query.shown = this.columnsToBinary(this.state.columns);
    }
    newState.columns = this.binaryToColumns(query.shown)

    if (query.page === undefined) { 
      query.page = this.state.page;
    }
    newState.page = parseInt(query.page, 10)

    if (query.limit === undefined) { 
      query.limit = this.state.limit;
    }
    newState.limit = parseInt(query.limit, 10)

    const stringified = queryString.stringify(query).replace('?', '');
    this.context.router.history.replace({
      search: stringified
    })

    this.setState(newState)
    this.refetch(newState.page, newState.limit)
  }

  async refetch(page, limit) {
    const query = queryString.parse(this.context.router.route.location.search)
    var httpQuery = '';
    Object.keys(query).forEach(k => {
      if (k !== 'shown' && k !== 'page' && k !== 'limit') {
        httpQuery += '&' + k + '=' + query[k];
      }
    });
    httpQuery += '&page=' + page + '&limit=' + limit
    const {data} = await axios.get(`http://instance1.cern.ch:5000/api/search?db_name=${this.props.dbName}` + httpQuery)
    this.setState({ page: page, totalRows: data.response.total_rows, rows: data.response.results })
    this.props.onDataFetched({rows: data.response.results });
  }

  handleChangePage = (event, page) => {
    if (page === 0 && this.state.rows.length === 0) {
      return
    } 
    const query = queryString.parse(this.context.router.route.location.search)
    query.page = page
    const stringified = queryString.stringify(query).replace('?', '');
    this.context.router.history.replace({
      search: stringified
    })
    this.setState({ page });
    this.refetch(page, this.state.limit)
  };

  handleChangeRowsPerPage = event => {
    var limit = event.target.value;
    const query = queryString.parse(this.context.router.route.location.search)
    query.page = 0
    query.limit = limit
    const stringified = queryString.stringify(query).replace('?', '');
    this.context.router.history.replace({
      search: stringified
    })
    this.setState({ page: 0, limit: limit });
    this.refetch(0, limit)
  };

  handleCheckboxChange = name => event => {
    var columns = [...this.state.columns]
    columns.forEach(entry => {
      if (entry.attrName === name) {
        entry.visible = event.target.checked === true ? 1 : 0
      }
    });
    this.setState({columns: columns});
    this.props.changeColumns({columns: columns});
    const query = queryString.parse(this.context.router.route.location.search)
    query.shown = this.columnsToBinary(columns);
    const stringified = queryString.stringify(query).replace('?', '');
    this.context.router.history.replace({
      search: stringified
    })
  };

  render() {
    return (
      <div>
        <Paper style={{margin: '5px'}} elevation={1}>
          {this.state.columns.map(attr => {
            return (
              <FormControlLabel control={
                <Checkbox
                  checked={attr.visible === 1}
                  onChange={this.handleCheckboxChange(attr.attrName)}
                  value={attr.displayName}
                />
              }
              key={attr.attrName}
              label={attr.displayName}
              style={{margin: '2px'}}/> 
            )
          })}
        </Paper>
        <Paper style={{margin: '5px'}} elevation={1}>
          <Table>
            <TableHead>
              <TableRow>
                {this.state.columns.filter(function (attr) {return attr.visible === 1}).map(attr => {
                  return (
                    <TableCell key={attr.attrName}>{attr.displayName}</TableCell>
                  )
                })}
              </TableRow>
            </TableHead>
            {this.props.children}
            <TableFooter>
              <TableRow>
                <TablePagination
                  count={this.state.totalRows}
                  rowsPerPage={this.state.limit}
                  page={this.state.page}
                  onChangePage={this.handleChangePage}
                  onChangeRowsPerPage={this.handleChangeRowsPerPage}
                />
              </TableRow>
            </TableFooter>
          </Table>
        </Paper>
      </div>
    )
  }
}

CampaignsPage.contextTypes = {
  router: PropTypes.object.isRequired
};

export default CampaignsPage
