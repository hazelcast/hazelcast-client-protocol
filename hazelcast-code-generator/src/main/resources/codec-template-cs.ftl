using Hazelcast.Client.Protocol;
using Hazelcast.Client.Protocol.Util;
using Hazelcast.IO;
using Hazelcast.IO.Serialization;
using System.Collections.Generic;

namespace ${model.packageName}
{
    internal sealed class ${model.className}
    {

        public static readonly ${model.parentName}MessageType RequestType = ${model.parentName}MessageType.${model.parentName?cap_first}${model.name?cap_first};
        public const int ResponseType = ${model.response};
        public const bool Retryable = <#if model.retryable == 1>true<#else>false</#if>;

        //************************ REQUEST *************************//

        public class RequestParameters
        {
            public static readonly ${model.parentName}MessageType TYPE = RequestType;
    <#list model.requestParams as param>
            public ${util.getCSharpType(param.type)} ${param.name};
    </#list>

            public static int CalculateDataSize(<#list model.requestParams as param>${util.getCSharpType(param.type)} ${param.name}<#if param_has_next>, </#if></#list>)
            {
                int dataSize = ClientMessage.HeaderSize;
                <#list model.requestParams as p>
                    <@sizeText var_name=p.name type=p.type isNullable=p.nullable/>
                </#list>
                return dataSize;
            }
        }

        public static ClientMessage EncodeRequest(<#list model.requestParams as param>${util.getCSharpType(param.type)} ${param.name}<#if param_has_next>, </#if></#list>)
        {
            int requiredDataSize = RequestParameters.CalculateDataSize(<#list model.requestParams as param>${param.name}<#if param_has_next>, </#if></#list>);
            ClientMessage clientMessage = ClientMessage.CreateForEncode(requiredDataSize);
            clientMessage.SetMessageType((int)RequestType);
            clientMessage.SetRetryable(Retryable);
            <#list model.requestParams as p>
                <@setterText var_name=p.name type=p.type isNullable=p.nullable/>
            </#list>
            clientMessage.UpdateFrameLength();
            return clientMessage;
        }

        //************************ RESPONSE *************************//


        public class ResponseParameters
        {
            <#list model.responseParams as param>
            public ${util.getCSharpType(param.type)} ${param.name};
            </#list>
        }

        public static ResponseParameters DecodeResponse(IClientMessage clientMessage)
        {
            ResponseParameters parameters = new ResponseParameters();
            <#list model.responseParams as p>
                <@getterText var_name=p.name type=p.type isNullable=p.nullable/>
            </#list>
            return parameters;
        }

    <#if model.events?has_content>

        //************************ EVENTS *************************//
        public abstract class AbstractEventHandler
        {
            public static void Handle(IClientMessage clientMessage, <#list model.events as event>Handle${event.name} handle${event.name}<#if event_has_next>, </#if></#list>)
            {
                int messageType = clientMessage.GetMessageType();
            <#list model.events as event>
                if (messageType == EventMessageConst.Event${event.name?cap_first}) {
                <#list event.eventParams as p>
                    <@getterText var_name=p.name type=p.type isNullable=p.nullable isEvent=true/>
                </#list>
                    handle${event.name}(<#list event.eventParams as param>${param.name}<#if param_has_next>, </#if></#list>);
                    return;
                }
            </#list>
                Hazelcast.Logging.Logger.GetLogger(typeof(AbstractEventHandler)).Warning("Unknown message type received on event handler :" + clientMessage.GetMessageType());
            }

        <#list model.events as event>
            public delegate void Handle${event.name}(<#list event.eventParams as param>${util.getCSharpType(param.type)} ${param.name}<#if param_has_next>, </#if></#list>);
        </#list>
       }

    </#if>
    }
}
<#--MACROS BELOW-->
<#--SIZE NULL CHECK MACRO -->
<#macro sizeText var_name type isNullable=false>
<#if isNullable>
                dataSize += Bits.BooleanSizeInBytes;
                if (${var_name} != null)
                {
</#if>
                    <@sizeTextInternal var_name=var_name type=type/>
<#if isNullable>
                }
</#if>
</#macro>

<#--SIZE MACRO -->
<#macro sizeTextInternal var_name type>
<#local cat= util.getTypeCategory(type)>
<#switch cat>
    <#case "OTHER">
        <#if util.isPrimitive(type)>
                dataSize += Bits.${type?cap_first}SizeInBytes;
        <#else >
                dataSize += ParameterUtil.CalculateDataSize(${var_name});
        </#if>
        <#break >
    <#case "CUSTOM">
                dataSize += ${util.getTypeCodec(type)?split(".")?last}.CalculateDataSize(${var_name});
        <#break >
    <#case "COLLECTION">
                dataSize += Bits.IntSizeInBytes;
        <#local genericType= util.getGenericType(type)>
        <#local n= var_name>
                foreach (var ${var_name}_item in ${var_name} )
                {
                    <@sizeText var_name="${n}_item" type=genericType/>
                }
        <#break >
    <#case "ARRAY">
                dataSize += Bits.IntSizeInBytes;
        <#local genericType= util.getArrayType(type)>
        <#local n= var_name>
                foreach (var ${var_name}_item in ${var_name} ) {
                    <@sizeText var_name="${n}_item"  type=genericType/>
                }
        <#break >
    <#case "MAP">
        <#local keyType = util.getFirstGenericParameterType(type)>
        <#local valueType = util.getSecondGenericParameterType(type)>
        <#local n= var_name>
                foreach (var entry in ${var_name}) {
                    var key = entry.Key;
                    var val = entry.Value;
                    <@sizeText var_name="key"  type=keyType/>
                    <@sizeText var_name="val"  type=valueType/>
                }
</#switch>
</#macro>

<#--SETTER NULL CHECK MACRO -->
<#macro setterText var_name type isNullable=false>
<#local isNullVariableName= "${var_name}_isNull">
<#if isNullable>
            bool ${isNullVariableName};
            if (${var_name} == null)
            {
                ${isNullVariableName} = true;
                clientMessage.Set(${isNullVariableName});
            }
            else
            {
                ${isNullVariableName}= false;
                clientMessage.Set(${isNullVariableName});
</#if>
                <@setterTextInternal var_name=var_name type=type/>
<#if isNullable>
            }
</#if>
</#macro>

<#--SETTER MACRO -->
<#macro setterTextInternal var_name type>
    <#local cat= util.getTypeCategory(type)>
    <#if cat == "OTHER">
            clientMessage.Set(${var_name});
    </#if>
    <#if cat == "CUSTOM">
            ${util.getTypeCodec(type)?split(".")?last}.Encode(${var_name}, clientMessage);
    </#if>
    <#if cat == "COLLECTION">
            clientMessage.Set(${var_name}.Count);
            <#local itemType= util.getGenericType(type)>
            <#local itemTypeVar= var_name + "_item">
            foreach (var ${itemTypeVar} in ${var_name}) {
                <@setterTextInternal var_name=itemTypeVar type=itemType/>
            }
    </#if>
    <#if cat == "ARRAY">
            clientMessage.Set(${var_name}.length);
            <#local itemType= util.getArrayType(type)>
            <#local itemTypeVar= var_name + "_item">
            foreach (var ${itemTypeVar} in ${var_name}) {
                <@setterTextInternal var_name=itemTypeVar  type=itemType/>
            }
    </#if>
    <#if cat == "MAP">
            <#local keyType = util.getFirstGenericParameterType(type)>
            <#local valueType = util.getSecondGenericParameterType(type)>
            clientMessage.Set(${var_name}.Count);
            foreach (var entry in ${var_name}) {
                var key = entry.Key;
                var val = entry.Value;
            <@setterTextInternal var_name="key"  type=keyType/>
            <@setterTextInternal var_name="val"  type=valueType/>
            }
    </#if>
</#macro>

<#--GETTER NULL CHECK MACRO -->
<#macro getterText var_name type isNullable=false isEvent=false>
            ${util.getCSharpType(type)} ${var_name} <#if !util.isPrimitive(type)>= null</#if>;
<#local isNullVariableName= "${var_name}_isNull">
<#if isNullable>
            bool ${isNullVariableName} = clientMessage.GetBoolean();
            if (!${isNullVariableName})
            {
</#if>
                <@getterTextInternal var_name=var_name varType=type/>
<#if !isEvent>
            parameters.${var_name} = ${var_name};
</#if>
<#if isNullable>
            }
</#if>
</#macro>

<#macro getterTextInternal var_name varType>
<#local cat= util.getTypeCategory(varType)>
<#switch cat>
    <#case "OTHER">
        <#switch varType>
            <#case util.DATA_FULL_NAME>
            ${var_name} = clientMessage.GetData();
                <#break >
            <#case "java.lang.Integer">
            ${var_name} = clientMessage.GetInt();
                <#break >
            <#case "java.lang.Boolean">
            ${var_name} = clientMessage.GetBoolean();
                <#break >
            <#case "java.lang.String">
            ${var_name} = clientMessage.GetStringUtf8();
                <#break >
            <#case "java.util.Map.Entry<com.hazelcast.nio.serialization.Data,com.hazelcast.nio.serialization.Data>">
            ${var_name} = clientMessage.GetMapEntry();
                <#break >
            <#default>
            ${var_name} = clientMessage.Get${util.capitalizeFirstLetter(varType)}();
        </#switch>
        <#break >
    <#case "CUSTOM">
            ${var_name} = ${util.getTypeCodec(varType)?split(".")?last}.Decode(clientMessage);
        <#break >
    <#case "COLLECTION">
    <#local collectionType><#if varType?starts_with("java.util.List")>List<#else>HashSet</#if></#local>
    <#local itemVariableType= util.getGenericType(varType)>
    <#local convertedItemType= util.getCSharpType(itemVariableType)>
    <#local itemVariableName= "${var_name}_item">
    <#local sizeVariableName= "${var_name}_size">
    <#local indexVariableName= "${var_name}_index">
            int ${sizeVariableName} = clientMessage.GetInt();
            ${var_name} = new ${collectionType}<${convertedItemType}>(${itemVariableType.startsWith("List")?then(sizeVariableName,"")});
            for (int ${indexVariableName} = 0; ${indexVariableName}<${sizeVariableName}; ${indexVariableName}++) {
                ${convertedItemType} ${itemVariableName};
                <@getterTextInternal var_name=itemVariableName varType=itemVariableType/>
                ${var_name}.Add(${itemVariableName});
            }
        <#break >
    <#case "ARRAY">
    <#local itemVariableType= util.getArrayType(varType)>
    <#local itemVariableName= "${var_name}_item">
    <#local sizeVariableName= "${var_name}_size">
    <#local indexVariableName= "${var_name}_index">
            int ${sizeVariableName} = clientMessage.getInt();
            ${var_name} = new ${itemVariableType}[${sizeVariableName}];
            for (int ${indexVariableName} = 0;${indexVariableName}<${sizeVariableName};${indexVariableName}++) {
                ${itemVariableType} ${itemVariableName};
                <@getterTextInternal var_name=itemVariableName varType=itemVariableType/>
                ${var_name}[${indexVariableName}] = ${itemVariableName};
            }
        <#break >
    <#case "MAP">
        <#local sizeVariableName= "${var_name}_size">
        <#local indexVariableName= "${var_name}_index">
        <#local keyType = util.getFirstGenericParameterType(varType)>
        <#local keyTypeCs = util.getCSharpType(keyType)>
        <#local valueType = util.getSecondGenericParameterType(varType)>
        <#local valueTypeCs = util.getCSharpType(valueType)>
        <#local keyVariableName= "${var_name}_key">
        <#local valVariableName= "${var_name}_val">
        int ${sizeVariableName} = clientMessage.GetInt();
        ${var_name} = new Dictionary<${keyTypeCs},${valueTypeCs}>(${sizeVariableName});
        for (int ${indexVariableName} = 0;${indexVariableName}<${sizeVariableName};${indexVariableName}++) {
            ${keyTypeCs} ${keyVariableName};
            ${valueTypeCs} ${valVariableName};
            <@getterTextInternal var_name=keyVariableName varType=keyType/>
            <@getterTextInternal var_name=valVariableName varType=valueType/>
            ${var_name}.Add(${keyVariableName}, ${valVariableName});
        }
</#switch>
</#macro>