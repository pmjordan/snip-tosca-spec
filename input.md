
The following code snippet shows an example node type definition:

```.yaml #s1
MyApp:
  derived_from: SoftwareComponent
  description: My company's custom application
  properties:
    my-app-password:
      type: string
      description: Application password
      validation:
        $and: 
        - { $greater_or_equal: [ $value, 6 ] }
        - { $less_or_equal: [ $value, 10 ] }
  attributes:
    my-app-port:
      type: integer
      description: Application port number
  requirements:
  - some-database:
      capability: EndPoint.Database
      node: Database    
      relationship: ConnectsTo
```

## 7.2 Node Template <a name=node-template></a>

A *node template* specifies the occurrence of one or more instances of
a component of a given type in an application or service. A node
template defines application-specific values for the properties,
relationships, or interfaces defined by its node type.

The following is the list of recognized keynames for a TOSCA node
template definition:

|Keyname|Mandatory|Type|Description|
| :---- | :------ | :---- | :------ |
|`type`|yes|str|The mandatory name of the [node type](#node-types) on which the node template is based.|
|`description`|no|str|An optional [description](#description) for the node template.|
|`metadata`|no|map of [metadata](#metadata)|Defines a section used to declare additional information. |
|`directives`|no|seq of strs|An optional list of [directive](#node-template-directives) values to provide processing instructions to orchestrators and tooling.|
|`properties`|no|map of [property assignments](#property-assignment)|An optional map of property value assignments for the node template.|
|`attributes`|no|map of [attribute assignments](#attribute-assignment)|An optional map of attribute value assignments for the node template.|
|`requirements`|no|seq of [requirement assignments](#requirement-assignment)|An optional list of requirement assignments for the node template.|
|`capabilities`|no|map of [capability assignments](#capabilities-assignment)|An optional map of capability assignments for the node template.|
|`interfaces`|no|map of [interface assignments](#interface-assignment)|An optional map of interface assignments for the node template.|
|`artifacts`|no|map of [artifact definitions](#artifact-definition)|An optional map of artifact definitions for the node template.|
|`count`|no|non-negative integer|An optional keyname that specifies how many [node representations](#specifying-number-of-node-representations) must be created from this node template. If not defined, the assumed count value is 1.|
|`node_filter`|no|[node filter](#node-filter-definition)|The optional filter definition that TOSCA orchestrators will use to select an already existing node if this node template is marked with the "select" directive.|
|`copy`|no|str|The optional (symbolic) name of another node template from which to copy all keynames and values into this node template.|

These keynames can be used according to the following grammar:

```yaml
<node_template_name>: 
  type: <node_type_name>
  description: <node_template_description>
  directives: [ <directive_1>, <directive_2>, ... ]
  metadata: 
    <metadata_name_1>: <metadata_value_1>
    <metadata_name_2>: <metadata_value_2>
    ...
  properties:
    <property_assignment_1>
    <property_assignment_2>
    ...
  attributes:
    <attribute_assignment_1>
    <attribute_assignment_2>
    ...
  requirements: 
  - <requirement_assignment_1>
  - <requirement_assignment_2>
  - ...
  capabilities:
    <capability_assignment_1>
    <capability_assignment_2>
    ...
  interfaces:
    <interface_assignment_1>
    <interface_assignment_2>
    ...
  artifacts:
    <artifact_def_1>
    <artifact_def_2>
    ...
  count: <node_count_value>
  node_filter: <node_filter_def>
  copy: <source_node_template_name>
```

In the above grammar, the placeholders that appear in angle brackets
have the following meaning:

- `<node_template_name>`: represents the mandatory symbolic name of the node
  template being defined.

- `<node_type_name>`: represents the name of the node type on which the
  node template is based.

- `<directive_*>`: represents the optional list of processing instruction
  values (as strings) for use by tooling and orchestrators. Valid
  directives supported by this version of the standard are "create",
  "select", and "substitute". If no directives are specified, "create"
  is used as the default value.

- `<property_assignment_*>`: represents the optional map of property
  assignments for the node template that provide values for properties
  defined in its declared node type.

- `<attribute_assignment_*>`: represents the optional map of attribute
  assignments for the node template that provide values for attributes
  defined in its declared node type.

- `<requirement_assignment_*>`: represents the optional list of requirement
  assignments for the node template for requirement definitions provided
  in its declared node type.

- `<capability_assignment_*>`: represents the optional map of capability
  assignments for the node template for capability definitions provided
  in its declared node type.

- `<interface_assignment_*>`: represents the optional map of interface
  assignments for the node template interface definitions provided in
  its declared node type.

- `<artifact_def_*>`: represents the optional map of artifact
  definitions for the node template that augment or replace those
  provided by its declared node type.

- `<node_count_value>`: represents the number of node representations that
  must be created from this node template. If not specified, a default
  value of 1 is used.

- `<node_filter_def>`: represents the optional node filter TOSCA
  orchestrators will use for selecting a matching node template.

- `<source_node_template_name>`: represents the optional (symbolic) name
  of another node template from which to copy all keynames and values
  into this node template. Note that he source node template provided
  as a value on the `copy` keyname MUST NOT itself use the `copy`
  keyname (i.e., it must itself be a complete node template
  description and not copied from another node template).

The following code snippet shows an example node template definition:

```.yaml #s1
node_templates:
  mysql:
    type: DBMS.MySQL
    properties:
      root-password: { $get_input: my-mysql-rootpw }
      port: { $get_input: my-mysql-port }
    requirements:
    - host: db-server
    interfaces:
      standard:
        operations:
          configure: scripts/my_own_configure.sh
```

### 7.2.1 Node Template Directives<a name=node-template-directives</a>

As described in the section above, a node template supports the following 3 directives 
used by the TOSCA resolver to populate nodes in the representation graph:

- "create" is the default directive, assumed if no directives are defined.
  The resolver is creating the node based on the node template with the specified
  properties, attributes, and interface implementations.

- "select" is the directive that specifies that a node from a representation graph
  external to this service should be selected and added into this service representation
  graph. The node is not duplicated and its properties, attributes, interfaces and outgoing
  relationships cannot be changed. Nevertheless, this node can become the target of incoming
  relationships within this representation graph. The symbolic name of the node is an alias
  by which this node is accessible in this representation graph.

  - The only keyname that is relevant for the resolver if the "select" directive is used is the
    `node_filter`, which is used to select a suitable node. All the others (e.g. property assignments,
    interface implementations, requirements, etc.) are ignored.

  - As the `node_filter` is only relevant for the "select" directive, it should not be present
    if the "select" directive is not present. Note that if the `node_filter` is missing then
    the selection will be based solely on the node type.

  - A detailed description of the `node_filter` is given in the [Node Filter Definition Section](#node-filter-definition).

- "substitute" is the directive that specifies that this node's realization and behavior
  should be realized by an internal service created from a substitution template.

  - A node representation for the substituted node will be created and added to the representation
    graph of the top-level service, and can be accessed in the top-level service via its symbolic name
    as any other node representation. Within the the top-level service scope none of the substitution
    service details are visible.

    - The substituted node properties are defined from the property assignments, its relationships are established from
      requirements, and the node can be target of other relationships.

  - A service is created from the substitution template having its own representation graph and associated to the
    substituted node in the top-level service.

     - The properties of the substituted node may become inputs to the substitution service if such a
       substitution mapping is defined.

     - The attributes of the substituted node will receive the output values of the substitution service
       if such substitution mapping is defined. Otherwise their value will remain undefined.

  - As the behavior of the substituted node is deferred to the substitution service, any implementation
    of the interfaces in the node template are ignored. To connect a behavior to the interface operations
    and notifications they or must be mapped to workflows in the substitution service (which then provide the "implementation").

  - A detailed description of the substitution mechanism is given in the [Substitution Section](#substitution).

Note that several directives can be specified in a list. The TOSCA resolver will attempt to use them in 
the right sequence. If not possible to fulfill the first in the list, it will try with the second, and so on.
For example `directives: select, substitute, create` means that first the resolver will try to find a node that
matches the `node_filter` within its available scope. If not found, it will try to find a suitable substitution
template that matches this node. If not found, it will finally try to create a new node from the node template 
definition.

## 7.3 Relationship Type <a name=relationship-type></a>

A *relationship type* is a reusable entity that defines the structure
of observable properties and attributes of a relationship as well as
its supported interfaces.

A relationship type definition is a type of TOSCA type definition and
as a result supports the common keynames listed in
[the section Common Keynames in Type Definitions](#common-keynames-in-type-definitions).
In addition, the relationship type definition has the following recognized keynames:

|Keyname|Mandatory|Definition/Type|Description|
| :---- | :------ | :---- | :------ |
|`properties`|no|map of [property definition](#property-definition)|An optional map of property definitions for the relationship type.|
|`attributes`|no|map of [attribute definitions](#attribute-definition)|An optional map of attribute definitions for the relationship type.|
|`interfaces`|no|map of [interface definitions](#interface-definition)|An optional map of interface definitions supported by the relationship type.|
|`valid_capability_types`|no|seq of strs|An optional list of one or more names of [capability types](#capability-types) that are valid targets for this relationship. If undefined, all capability types are valid.|
|`valid_target_node_types`|no|seq of strs|An optional list of one or more names of [node types](#node_types) that are valid targets for this relationship. If undefined, all node types are valid targets.|
|`valid_source_node_types`|no|seq of strs|An optional list of one or more names of [node types](#node_types) that are valid sources for this relationship. If undefined, all node types are valid sources.|

These keynames can be used according to the following grammar:

```yaml
<relationship_type_name>:
  derived_from: <parent_relationship_type_name>
  version: <version_number>
  metadata: 
    <metadata_name_1>: <metadata_value_1>
    <metadata_name_2>: <metadata_value_2>
    ...
  description: <relationship_description>
  properties:
    <property_def_1>
    <property_def_2>
    ...
  attributes:
    <attribute_def_1>
    <attribute_def_2>
    ...
  interfaces: 
    <interface_def_1>
    <interface_def_2>
    ...
  valid_capability_types: [ <capability_type_name_1>, <capability_type_name_2>, ... ]
  valid_target_node_types: [ <target_node_type_name_1>, <target_node_type_name_2>, ... ]
  valid_source_node_types: [ <source_node_type_name_1>, <source_node_type_name_2>, ... ]
```

In the above grammar, the placeholders that appear in angle brackets
have the following meaning:

- `<relationship_type_name>`: represents the mandatory symbolic name of the
  relationship type being declared as a string.

- `<parent_relationship_type_name>`: represents the name (string) of the
  relationship type from which this relationship type definition
  derives (i.e., its "parent" type). Parent node type names can be
  qualified using a namespace prefix.

- `<property_def_*>`: represents the optional map of property
  definitions for the relationship type.

- `<attribute_def_*>`: represents the optional map of attribute
  definitions for the relationship type.

- `<interface_def_*>`: represents the optional map of interface
  definitions supported by the relationship type.

- `<capability_type_name_*>`: represents the optional list of valid target
  capability types for the relationship. Target capability type names
  can be qualified using a namespace prefix. If undefined, the valid
  target types are not restricted at all (i.e., all capability types
  are valid).

- `<target_node_type_name_*>`: represents the optional list of valid target
  node types for the relationship. Target node type names can be
  qualified using a namespace prefix. If undefined, the valid types
  are not restricted at all (i.e., all node types are valid).

- `<source_node_type_name_*>`: represents the optional list of valid source
  node types for the relationship. Source node type names can be
  qualified using a namespace prefix. If undefined, the valid types
  are not restricted at all (i.e., all node types are valid).

During relationship type derivation the keyname definitions follow these
rules:

- `properties`: existing property definitions may be refined; new property
  definitions may be added.

- `attributes`: existing attribute definitions may be refined; new
  attribute definitions may be added.

- `interfaces`: existing interface definitions may be refined; new
  interface definitions may be added.

- `valid_capability_types`: A derived type is only allowed to further
  restrict the list of valid capability types, not to expand it. This
  means that if `valid_capability_types` is defined in the parent type,
  each element in the derived type's list of valid capability types
  must either be in the parent type list or derived from an element in
  the parent type list; if `valid_target_types` is not defined in the
  parent type then no derivation restrictions need to be applied.

- `valid_target_node_types`: same derivation rules as for
  `valid_capability_types`

- `valid_source_node_types`: same derivation rules as for
  `valid_capability_types`

The following code snippet shows an example relationship type definition:

```.yaml #s1
AppDependency:
  derived_from: DependsOn
  valid_capability_types: [ SomeAppFeature ]
```

## 7.4 Relationship Template <a name=relationship-template></a>

A *relationship template* specifies the occurrence of a relationship
of a given type between nodes in an application or service.  A
relationship template defines application-specific values for the
properties, relationships, or interfaces defined by its relationship
type.

TOSCA allows relationships between nodes to be defined *inline* using
requirement assignments within node templates or *out-of-band* using
relationship templates as defined in this section. While the use of
requirement assignments is more common, the use of relationship
templates decouples relationship definitions from specific node
templates, allowing reuse of these relationship templates by multiple
node templates. Relationship templates are local within a service
template and so have a limited scope.

Note that relationship template grammar is underspecified currently
and needs further work.

The following is the list of recognized keynames for a TOSCA
relationship template definition:

|Keyname|Mandatory|Type|Description|
| :---- | :------ | :---- | :------ |
|`type`|yes|str|The mandatory name of the [relationship type](#relationship-types) on which the relationship template is based.|
|`description`|no|str|An optional [description](#description) for the relationship template.|
|`metadata`|no|map of [metadata](#metadata)|Defines a section used to declare additional information. |
|`properties`|no|map of [property assignments](#property-definition)|An optional map of property assignments for the relationship template.|
|`attributes`|no|map of [attribute assignments](#attribute-definition)|An optional map of attribute assignments for the relationship template.|
|`interfaces`|no|map of [interface assignments](#interface-assignment)|An optional map of interface assignments for the relationship template.|
|`copy`|no|str|The optional (symbolic) name of another relationship template from which to copy all keynames and values into this relationship template.|

These keynames can be used according to the following grammar:

```yaml
<relationship_template_name>: 
  type: <relationship_type_name>
  description: <relationship_type_description>
  metadata: 
    <metadata_name_1>: <metadata_value_1>
    <metadata_name_2>: <metadata_value_2>
    ...
  properties:
    <property_assignment_1>
    <property_assignment_2>
    ...
  attributes:
    <attribute_assignment_1>
    <attribute_assignment_2>
    ...
  interfaces:
    <interface_assignment_1>
    <interface_assignment_2>
    ...
  copy: <source_relationship_template_name>
```

In the above grammar, the placeholders that appear in angle brackets
have the following meaning:

- `<relationship_template_name>`: represents the mandatory symbolic name of
  the relationship template being declared.

- `<relationship_type_name>`: represents the name of the relationship type
  the relationship template is based upon.

- `<relationship_template_description>`: represents the optional description
  string for the relationship template.

- `<property_assignment_*>`: represents the optional map of property
  assignments for the relationship template that provide values for
  properties defined in its declared relationship type.

- `<attribute_assignment_*>`: represents the optional map of attribute
  assignments for the relationship template that provide values for
  attributes defined in its declared relationship type.

- `<interface_assignment_*>`: represents the optional map of interface
  assignments for the relationship template for interface definitions
  provided by its declared relationship type.

- `<source_relationship_template_name>`: represents the optional (symbolic)
  name of another relationship template to copy into (all keynames and
  values) and use as a basis for this relationship template.

- `<source_relationship_template_name>`: represents the optional
  (symbolic) name of another relationship template from which to copy
  all keynames and values into this relationship template. Note that
  he source relationship template provided as a value on the `copy`
  keyname MUST NOT itself use the `copy` keyname (i.e., it must
  itself be a complete relationship template description and not
  copied from another relationship template).

The following code snippet shows an example relationship template definition:

```.yaml #s1
relationship_templates:
  storage-attachment:
    type: AttachesTo
    properties:
      location: /my_mount_point
```
