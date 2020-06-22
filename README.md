# jupyter-sfdxmagic

## Description

This is a set of cell magics to run anonymous APEX code in notebooks and perform SOQL queries returning the records in a pandas DataFrame.

## Prerequisite

The connection to Salesforce are performed through sfdx, the magic assume sfdx is correctly installed and at least the default organization has been authorized.

The module assumes to be in the same environment where `jupyterlab` is installed

## Installation

Through pip

```
$ pyhthon -m pip install sfdxmagic
```


## Usage

To load the extension:

```
%load_ext sfdxmagic
```

### `%%sfdx:apex`

Runs anonymous APEX:

```
%%sfdx:apex
System.debug('hello world!');
```

Append the name of a variable to return the log lines as a list

```
%%sfdx:apex logs
...
```

### `%%sfdx:query`

Perform a SOQL query:

```
%%sfdx:query
SELECT Id, Name FROM Lead LIMIT 10
```

Append the name of a variable to return the records as a pandas DataFrame

```
%%sfdx:query df_records
...
```

### General invocation

Parameters passed to the commands are forwarded to the sfdx cli, this allows to retrieve results from multiple organizations in the same notebook.

```
%%sfdx:query df_records_org1 --targetusername username@domain.com.org1
...
```

```
%%sfdx:query df_records_org2 --targetusername username@domain.com.org2
...
```

## Known issues

- Missing subquery handling, results are not unpacked and the projection is lost

## License

MIT

