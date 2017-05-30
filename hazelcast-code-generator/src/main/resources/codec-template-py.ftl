from hazelcast.serialization.bits import *
from hazelcast.protocol.client_message import ClientMessage
from hazelcast.protocol.custom_codec import *
from hazelcast.util import ImmutableLazyDataList
from hazelcast.protocol.codec.${util.convertToSnakeCase(model.parentName)}_message_type import *
<#if model.events?has_content>
from hazelcast.protocol.event_response_const import *
</#if>

REQUEST_TYPE = ${model.parentName?upper_case}_${model.name?upper_case}
RESPONSE_TYPE = ${model.response}
RETRYABLE = <#if model.retryable == 1>True<#else>False</#if>

<#--************************ REQUEST ********************************************************-->

def calculate_size(<#list model.requestParams as param>${util.convertToSnakeCase(param.name)}<#if param_has_next>, </#if></#list>):
    """ Calculates the request payload size"""
    data_size = 0
<#list model.requestParams as p>
    <@sizeText var_name=util.convertToSnakeCase(p.name) type=p.type isNullable=p.nullable/>
</#list>
    return data_size


def encode_request(<#list model.requestParams as param>${util.convertToSnakeCase(param.name)}<#if param_has_next>, </#if></#list>):
    """ Encode request into client_message"""
    client_message = ClientMessage(payload_size=calculate_size(<#list model.requestParams as param>${util.convertToSnakeCase(param.name)}<#if param_has_next>, </#if></#list>))
    client_message.set_message_type(REQUEST_TYPE)
    client_message.set_retryable(RETRYABLE)
<#list model.requestParams as p>
<@setterText var_name=util.convertToSnakeCase(p.name) type=p.type isNullable=p.nullable/>
</#list>
    client_message.update_frame_length()
    return client_message


<#--************************ RESPONSE ********************************************************-->
<#if model.responseParams?has_content>
def decode_response(client_message, to_object=None):
    """ Decode response from client message"""
    parameters = dict(<#list model.responseParams as p>${util.convertToSnakeCase(p.name)}=None<#if p_has_next>, </#if></#list>)
<#list model.responseParams as p>
<@getterText var_name=util.convertToSnakeCase(p.name) type=p.type isNullable=p.nullable indent=1/>
</#list>
    return parameters
<#else>
# Empty decode_response(client_message), this message has no parameters to decode
</#if>


<#--************************ EVENTS ********************************************************-->
<#if model.events?has_content>
def handle(client_message, <#list model.events as event>handle_event_${event.name?lower_case} = None<#if event_has_next>, </#if></#list>, to_object=None):
    """ Event handler """
    message_type = client_message.get_message_type()
    <#list model.events as event>
    if message_type == EVENT_${event.name?upper_case} and handle_event_${event.name?lower_case} is not None:
        <#list event.eventParams as p>
<@getterText var_name=util.convertToSnakeCase(p.name) type=p.type isNullable=p.nullable isEvent=true indent=2/>
        </#list>
        handle_event_${event.name?lower_case}(<#list event.eventParams as param>${util.convertToSnakeCase(param.name)}=${util.convertToSnakeCase(param.name)}<#if param_has_next>, </#if></#list>)
    </#list>
</#if>

<#--MACROS BELOW-->
<#--SIZE NULL CHECK MACRO -->
<#macro sizeText var_name type isNullable=false>
<#if isNullable>
    data_size += BOOLEAN_SIZE_IN_BYTES
    if ${var_name} is not None:
<@sizeTextInternal var_name=var_name type=type indent=2/>
<#else>
<@sizeTextInternal var_name=var_name type=type indent=1/>
</#if>
</#macro>


<#--METHOD PARAM MACRO -->
<#macro methodParam type><#local cat= util.getTypeCategory(type)>
<#switch cat>
<#case "COLLECTION"><#local genericType= util.getGenericType(type)>java.util.Collection<${genericType}><#break>
<#default>${type}
</#switch>
</#macro>

<#--SIZE MACRO -->
<#macro sizeTextInternal var_name type indent>
<#local cat= util.getTypeCategory(type)>
<#switch cat>
    <#case "OTHER">
        <#if util.isPrimitive(type)>
${""?left_pad(indent * 4)}data_size += ${type?upper_case}_SIZE_IN_BYTES
        <#else >
${""?left_pad(indent * 4)}data_size += calculate_size_${util.getPythonType(type)?lower_case}(${var_name})
        </#if>
        <#break >
    <#case "CUSTOM">
${""?left_pad(indent * 4)}data_size += calculate_size_${util.getPythonType(type)?lower_case}(${var_name})
        <#break >
    <#case "COLLECTION">
${""?left_pad(indent * 4)}data_size += INT_SIZE_IN_BYTES
        <#local genericType= util.getGenericType(type)>
        <#local n= var_name>
${""?left_pad(indent * 4)}for ${var_name}_item in ${var_name}:
        <@sizeTextInternal var_name="${n}_item"  type=genericType indent=(indent + 1)/>
        <#break >
    <#case "ARRAY">
${""?left_pad(indent * 4)}data_size += INT_SIZE_IN_BYTES
        <#local genericType= util.getArrayType(type)>
        <#local n= var_name>
${""?left_pad(indent * 4)}for ${var_name}_item in ${var_name}:
        <@sizeTextInternal var_name="${n}_item"  type=genericType indent=(indent + 1)/>
        <#break >
    <#case "MAP">
        <#local keyType = util.getFirstGenericParameterType(type)>
        <#local valueType = util.getSecondGenericParameterType(type)>
        <#local n= var_name>
${""?left_pad(indent * 4)}for key, val in ${var_name}.iteritems():
        <@sizeTextInternal var_name="key"  type=keyType indent=(indent + 1)/>
        <@sizeTextInternal var_name="val"  type=valueType indent=(indent + 1)/>
</#switch>
</#macro>

<#--SETTER NULL CHECK MACRO -->
<#macro setterText var_name type isNullable=false>
<#local isNullVariableName= "${var_name}_is_null">
<#if isNullable>
    client_message.append_bool(${var_name} is None)
    if ${var_name} is not None:
<@setterTextInternal var_name=var_name type=type indent=2/>
<#else>
<@setterTextInternal var_name=var_name type=type indent=1/>
</#if>
</#macro>

<#--SETTER MACRO -->
<#macro setterTextInternal var_name type indent>
    <#local cat= util.getTypeCategory(type)>
    <#if cat == "OTHER">
${""?left_pad(indent * 4)}client_message.append_${util.getPythonType(type)?lower_case}(${var_name})
    </#if>
    <#if cat == "CUSTOM">
${""?left_pad(indent * 4)}${util.getTypeCodec(type)?split(".")?last}.encode(client_message, ${var_name})
    </#if>
    <#if cat == "COLLECTION">
${""?left_pad(indent * 4)}client_message.append_int(len(${var_name}))
        <#local itemType= util.getGenericType(type)>
        <#local itemTypeVar= var_name + "_item">
${""?left_pad(indent * 4)}for ${itemTypeVar} in ${var_name}:
    <@setterTextInternal var_name=itemTypeVar type=itemType indent=(indent + 1)/>
    </#if>
    <#if cat == "ARRAY">
${""?left_pad(indent * 4)}client_message.append_int(len(${var_name}))
        <#local itemType= util.getArrayType(type)>
        <#local itemTypeVar= var_name + "_item">
${""?left_pad(indent * 4)}for ${itemTypeVar} in ${var_name}:
    <@setterTextInternal var_name=itemTypeVar  type=itemType indent=(indent + 1)/>
    </#if>
    <#if cat == "MAP">
        <#local keyType = util.getFirstGenericParameterType(type)>
        <#local valueType = util.getSecondGenericParameterType(type)>
${""?left_pad(indent * 4)}client_message.append_int(len(${var_name}))
${""?left_pad(indent * 4)}for key, value in ${var_name}.iteritems():
    <@setterTextInternal var_name="key"  type=keyType indent=(indent + 1)/>
    <@setterTextInternal var_name="value"  type=valueType indent=(indent + 1)/>
    </#if>
</#macro>

<#--GETTER NULL CHECK MACRO -->
<#macro getterText var_name type isNullable=false isEvent=false indent=1>
<#if isNullable>
${""?left_pad(indent * 4)}${var_name}=None
${""?left_pad(indent * 4)}if not client_message.read_bool():
<@getterTextInternal var_name=var_name varType=type isEvent=isEvent indent=indent +1/>
<#else>
<@getterTextInternal var_name=var_name varType=type isEvent=isEvent indent= indent/>
</#if>
</#macro>

<#macro getterTextInternal var_name varType indent isEvent=false isCollection=false>
<#local cat= util.getTypeCategory(varType)>
<#local isDeserial= !(isEvent || isCollection)>
<#switch cat>
    <#case "OTHER">
        <#switch varType>
            <#case util.DATA_FULL_NAME>
${""?left_pad(indent * 4)}<#if !(isEvent || isCollection)>parameters['${var_name}']<#else>${var_name}</#if> = <#if isDeserial>to_object(</#if>client_message.read_data()<#if isDeserial>)</#if>
                <#break >
            <#case "java.lang.Integer">
${""?left_pad(indent * 4)}<#if !(isEvent || isCollection)>parameters['${var_name}']<#else>${var_name}</#if> = client_message.read_int()
                <#break >
            <#case "java.lang.Boolean">
${""?left_pad(indent * 4)}<#if !(isEvent || isCollection)>parameters['${var_name}']<#else>${var_name}</#if> = client_message.read_bool()
                <#break >
            <#case "java.lang.String">
${""?left_pad(indent * 4)}<#if !(isEvent || isCollection)>parameters['${var_name}']<#else>${var_name}</#if> = client_message.read_str()
                <#break >
            <#case "java.util.Map.Entry<com.hazelcast.nio.serialization.Data,com.hazelcast.nio.serialization.Data>">
${""?left_pad(indent * 4)}<#if !(isEvent || isCollection)>parameters['${var_name}']<#else>${var_name}</#if> = (<#if isDeserial>to_object(</#if>client_message.read_data()<#if isDeserial>)</#if>, <#if isDeserial>to_object(</#if>client_message.read_data()<#if isDeserial>)</#if>)
                <#break >
            <#default>
${""?left_pad(indent * 4)}<#if !(isEvent || isCollection)>parameters['${var_name}']<#else>${var_name}</#if> = client_message.read_${util.getPythonType(varType)}()
        </#switch>
        <#break >
    <#case "CUSTOM">
${""?left_pad(indent * 4)}<#if !(isEvent || isCollection)>parameters['${var_name}']<#else>${var_name}</#if> = ${util.getTypeCodec(varType)?split(".")?last}.decode(client_message, to_object)
        <#break >
    <#case "COLLECTION">
    <#case "ARRAY">
    <#if cat == "COLLECTION">
    <#local itemVariableType= util.getGenericType(varType)>
    <#else>
    <#local itemVariableType= util.getArrayType(varType)>
    </#if>

    <#local itemVariableName= "${var_name}_item">
    <#local sizeVariableName= "${var_name}_size">
    <#local indexVariableName= "${var_name}_index">
${""?left_pad(indent * 4)}${sizeVariableName} = client_message.read_int()
${""?left_pad(indent * 4)}${var_name} = []
${""?left_pad(indent * 4)}for ${indexVariableName} in xrange(0, ${sizeVariableName}):
                            <@getterTextInternal var_name=itemVariableName varType=itemVariableType isEvent=isEvent isCollection=true indent=(indent +1)/>
${""?left_pad(indent * 4)}    ${var_name}.append(${itemVariableName})
<#if !(isEvent || isCollection)>
${""?left_pad(indent * 4)}parameters['${var_name}'] = ImmutableLazyDataList(${var_name}, to_object)
</#if>
        <#break >
    <#case "MAP">
        <#local sizeVariableName= "${var_name}_size">
        <#local indexVariableName= "${var_name}_index">
        <#local keyType = util.getFirstGenericParameterType(varType)>
        <#local valueType = util.getSecondGenericParameterType(varType)>
        <#local keyVariableName= "${var_name}_key">
        <#local valVariableName= "${var_name}_val">
${""?left_pad(indent * 4)}${sizeVariableName} = client_message.read_int()
${""?left_pad(indent * 4)}${var_name} = {}
${""?left_pad(indent * 4)}for ${indexVariableName} in xrange(0,${sizeVariableName}):
            <@getterTextInternal var_name=keyVariableName varType=keyType isEvent=true indent=(indent +1)/>
            <@getterTextInternal var_name=valVariableName varType=valueType isEvent=true indent=(indent +1)/>
${""?left_pad(indent * 4)}    ${var_name}[${keyVariableName}] = ${valVariableName}
${""?left_pad(indent * 4)}<#if !isEvent>parameters['${var_name}'] = ${var_name}</#if>
</#switch>
</#macro>
