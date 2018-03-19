/*
 * Copyright (c) 2008-2018, Hazelcast, Inc. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/* tslint:disable */
import ClientMessage = require('../ClientMessage');
import {BitsUtil} from '../BitsUtil';
import Address = require('../Address');
import {AddressCodec} from './AddressCodec';
import {UUIDCodec} from './UUIDCodec';
import {MemberCodec} from './MemberCodec';
import {Data} from '../serialization/Data';
import {EntryViewCodec} from './EntryViewCodec';
import DistributedObjectInfoCodec = require('./DistributedObjectInfoCodec');
import {Member} from '../core/Member';
import {UUID} from '../core/UUID';
import {${model.parentName}MessageType} from './${model.parentName}MessageType';

var REQUEST_TYPE = ${model.parentName}MessageType.${model.parentName?upper_case}_${model.name?upper_case};
var RESPONSE_TYPE = ${model.response};
var RETRYABLE = <#if model.retryable == 1>true<#else>false</#if>;

<#--************************ REQUEST ********************************************************-->

export class ${model.className} {
    static calculateSize(<#list model.requestParams as param>${util.convertSpecialNodeName(param.name)} : ${util.getTsType(param.type)} <#if param_has_next> , </#if></#list>){
        var dataSize : number = 0;
        <#list model.requestParams as p>
            <@sizeText var_name=util.convertSpecialNodeName(p.name) type=p.type isNullable=p.nullable/>
        </#list>
        return dataSize;
    }

    static encodeRequest(<#list model.requestParams as param>${util.convertSpecialNodeName(param.name)} : ${util.getTsType(param.type)}<#if param_has_next>, </#if></#list>){
        var clientMessage = ClientMessage.newClientMessage(this.calculateSize(<#list model.requestParams as param>${util.convertSpecialNodeName(param.name)}<#if param_has_next>, </#if></#list>));
        clientMessage.setMessageType(REQUEST_TYPE);
        clientMessage.setRetryable(RETRYABLE);
        <#list model.requestParams as p>
            <@setterText var_name=util.convertSpecialNodeName(p.name) type=p.type isNullable=p.nullable/>
        </#list>
        clientMessage.updateFrameLength();
        return clientMessage;
    }

<#--************************ RESPONSE ********************************************************-->
<#if model.responseParams?has_content>
    static decodeResponse(clientMessage : ClientMessage,  toObjectFunction: (data: Data) => any = null){
    <#assign messageVersion=model.messageSinceInt>
        var parameters :any = {
    <#list model.responseParams as p>
            '${util.convertSpecialNodeName(p.name)}' : null <#if p_has_next>, </#if>
    </#list>
        };

    <#list model.responseParams as p>
        <#if p.versionChanged>
        if (clientMessage.isComplete() ) {
            return parameters;
        }
        </#if>
        <@getterText var_name=util.convertSpecialNodeName(p.name) type=p.type isNullable=p.nullable/>
        <#if p.sinceVersionInt gt messageVersion >parameters.${util.convertSpecialNodeName(p.name)}Exist = true;</#if>
    </#list>
    return parameters;
    }
<#else>
// Empty decodeResponse(ClientMessage), this message has no parameters to decode
</#if>

<#--************************ EVENTS ********************************************************-->
<#if model.events?has_content>
    static handle(clientMessage : ClientMessage, <#list model.events as event>handleEvent${util.capitalizeFirstLetter(event.name?lower_case)} : any<#if event_has_next>, </#if></#list> ,toObjectFunction: (data: Data) => any = null){
        var messageType = clientMessage.getMessageType();
    <#list model.events as event>
        if ( messageType === BitsUtil.EVENT_${event.name?upper_case} && handleEvent${util.capitalizeFirstLetter(event.name?lower_case)} !== null) {
            var messageFinished = false;
        <#list event.eventParams as p>
            var ${util.convertSpecialNodeName(p.name)} : ${util.getTsType(p.type)} = undefined;
        <#if p.versionChanged >
            if (!messageFinished) {
                messageFinished = clientMessage.isComplete();
            }
        </#if>
            if (!messageFinished) {
            <@getterText var_name=util.convertSpecialNodeName(p.name) type=p.type isNullable=p.nullable isEvent=true isDefined=true />
            }
        </#list>
        handleEvent${util.capitalizeFirstLetter(event.name?lower_case)}(<#list event.eventParams as param>${util.convertSpecialNodeName(param.name)}<#if param_has_next>, </#if></#list>);
        }
    </#list>
    }
</#if>
}
<#--MACROS BELOW-->
<#--SIZE NULL CHECK MACRO -->
<#macro sizeText var_name type isNullable=false>
<#if isNullable>
    dataSize += BitsUtil.BOOLEAN_SIZE_IN_BYTES;
    if(${var_name} !== null) {
        <@sizeTextInternal var_name=var_name type=type/>
    }
<#else>
<@sizeTextInternal var_name=var_name type=type/>
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
<#macro sizeTextInternal var_name type>
    <#local cat=util.getTypeCategory(type)>
    <#switch cat>
        <#case "OTHER">
            <#if util.isPrimitive(type)>
        dataSize += BitsUtil.${type?upper_case}_SIZE_IN_BYTES;
            <#else >
            <#switch type>
                <#case "java.lang.Integer">
        dataSize += BitsUtil.INT_SIZE_IN_BYTES;
                    <#break >
                <#case "java.lang.Long">
        dataSize += BitsUtil.LONG_SIZE_IN_BYTES;
                    <#break >
                <#default>
        dataSize += BitsUtil.calculateSize${util.capitalizeFirstLetter(util.getTsType(type)?lower_case)}(${var_name});
            </#switch>
        </#if>
            <#break >
        <#case "CUSTOM">
        dataSize += BitsUtil.calculateSize${util.capitalizeFirstLetter(util.getTsType(type)?lower_case)}(${var_name});
            <#break >
        <#case "COLLECTION">
        dataSize += BitsUtil.INT_SIZE_IN_BYTES;
            <#local genericType=util.getGenericType(type)>
            <#local n= var_name>

        ${var_name}.forEach((${var_name}Item : ${util.getTsType(genericType)}) => {
            <@sizeTextInternal var_name="${n}Item"  type=genericType />
        });
            <#break >
        <#case "ARRAY">
        dataSize += BitsUtil.INT_SIZE_IN_BYTES
            <#local genericType= util.getArrayType(type)>
            <#local n= var_name>
        ${var_name}.forEach((${var_name}Item : any) => {
            <@sizeTextInternal var_name="${n}Item"  type=genericType />
        });
            <#break >
        <#case "MAP">
            <#local keyType = util.getFirstGenericParameterType(type)>
            <#local valueType = util.getSecondGenericParameterType(type)>
            <#local n= var_name>
        ${var_name}.forEach((entry : any) => {
            <@sizeTextInternal var_name="entry.key"  type=keyType />
            <@sizeTextInternal var_name="entry.val"  type=valueType />
        });
    <#break >
        <#case "MAPENTRY">
            <#local keyType = util.getFirstGenericParameterType(type)>
            <#local valueType = util.getSecondGenericParameterType(type)>
            <#local n= var_name>
        var key : ${util.getTsType(keyType)} =  ${var_name}[0];
        var val : ${util.getTsType(valueType)} = ${var_name}[1];
            <@sizeText var_name="key"  type=keyType/>
            <@sizeText var_name="val"  type=valueType/>
    </#switch>
</#macro>

<#--SETTER NULL CHECK MACRO -->
<#macro setterText var_name type isNullable=false>
    <#local isNullVariableName= "${var_name}IsNull">
    <#if isNullable>
    clientMessage.appendBoolean(${var_name} === null);
    if(${var_name} !== null){
        <@setterTextInternal var_name=var_name type=type />
    }
    <#else>
        <@setterTextInternal var_name=var_name type=type />
    </#if>
</#macro>

<#--SETTER MACRO -->
<#macro setterTextInternal var_name type >
    <#local cat= util.getTypeCategory(type)>
    <#if cat == "OTHER">
        <#switch type>
            <#case "java.lang.Integer">
                clientMessage.appendInt32(${var_name});
                <#break >
            <#case "int">
                clientMessage.appendInt32(${var_name});
                <#break >
            <#case "byte">
                clientMessage.appendByte(${var_name});
                <#break >
            <#case "java.lang.Long">
                clientMessage.appendLong(${var_name});
                <#break >
            <#case "long">
                clientMessage.appendLong(${var_name});
                <#break >
            <#default>
                clientMessage.append${util.capitalizeFirstLetter(util.getTsType(type))}(${var_name});
        </#switch>
    </#if>
    <#if cat == "CUSTOM">
    ${util.getTypeCodec(type)?split(".")?last}.encode(clientMessage, ${var_name});
    </#if>
    <#if cat == "COLLECTION">
    clientMessage.appendInt32(${var_name}.length);
        <#local itemType= util.getGenericType(type)>
        <#local itemTypeVar= var_name + "Item">

    ${var_name}.forEach((${itemTypeVar} : any) => {
        <@setterTextInternal var_name=itemTypeVar type=itemType />
    });

    </#if>
    <#if cat == "ARRAY">
    clientMessage.appendInt32(${var_name}.length);
        <#local itemType= util.getArrayType(type)>
        <#local itemTypeVar= var_name + "Item">

    ${var_name}.forEach((${itemTypeVar} : any) => {
        <@setterTextInternal var_name=itemTypeVar type=itemType />
    });

    </#if>
    <#if cat == "MAP">
        <#local keyType = util.getFirstGenericParameterType(type)>
        <#local valueType = util.getSecondGenericParameterType(type)>
    clientMessage.appendInt32(${var_name}.length);
    ${var_name}.forEach((entry : any) => {
        <@setterTextInternal var_name="entry.key"  type=keyType />
        <@setterTextInternal var_name="entry.val"  type=valueType />
    });
    </#if>
    <#if cat == "MAPENTRY">
        <#local keyType = util.getFirstGenericParameterType(type)>
        <#local valueType = util.getSecondGenericParameterType(type)>
    var key : ${util.getTsType(keyType)} = ${var_name}[0];
    var val : ${util.getTsType(valueType)}  = ${var_name}[1];
        <@setterTextInternal var_name="key"  type=keyType/>
        <@setterTextInternal var_name="val"  type=valueType/>
    </#if>
</#macro>

<#--GETTER NULL CHECK MACRO -->
<#macro getterText var_name type isNullable=false isEvent=false isDefined=false >
    <#if isNullable>

    if(clientMessage.readBoolean() !== true){
        <@getterTextInternal var_name=var_name varType=type isEvent=isEvent isDefined=isDefined />
    }
    <#else>
        <@getterTextInternal var_name=var_name varType=type isEvent=isEvent isDefined=isDefined />
    </#if>
</#macro>

<#macro getterTextInternal var_name varType isEvent isDefined=false isCollection=false>
    <#local cat= util.getTypeCategory(varType)>
    <#local isDeserial= !(isEvent || isCollection)>
    <#switch cat>
        <#case "OTHER">
            <#switch varType>
                <#case util.DATA_FULL_NAME>
                    <#if !isEvent>parameters['${var_name}']<#else>${var_name}</#if> = <#if isDeserial>toObjectFunction(</#if>clientMessage.readData()<#if isDeserial>)</#if>;
                    <#break >
                <#case "java.lang.Integer">
                    <#if !isEvent>parameters['${var_name}']<#else>${var_name}</#if> = clientMessage.readInt32();
                    <#break >
                <#case "int">
                    <#if !isEvent>parameters['${var_name}']<#else>${var_name}</#if> = clientMessage.readInt32();
                    <#break >
                <#case "byte">
                    <#if !isEvent>parameters['${var_name}']<#else>${var_name}</#if> = clientMessage.readByte();
                    <#break >
                <#case "java.lang.Long">
                    <#if !isEvent>parameters['${var_name}']<#else>${var_name}</#if> = clientMessage.readLong();
                    <#break >
                <#case "long">
                    <#if !isEvent>parameters['${var_name}']<#else>${var_name}</#if> = clientMessage.readLong();
                    <#break >
                <#case "java.lang.Boolean">
                    <#if !isEvent>parameters['${var_name}']<#else>${var_name}</#if> = clientMessage.readBoolean();
                    <#break >
                <#case "java.lang.String">
                    <#if !isEvent>parameters['${var_name}']<#else>${var_name}</#if> = clientMessage.readString();
                    <#break >
                <#case "java.util.Map.Entry<com.hazelcast.nio.serialization.Data,com.hazelcast.nio.serialization.Data>">
                    <#if !isEvent>parameters['${var_name}']<#else>${var_name}</#if> = [<#if isDeserial>toObjectFunction(</#if>clientMessage.readData()<#if isDeserial>)</#if>, <#if isDeserial>toObjectFunction(</#if>clientMessage.readData()<#if isDeserial>)</#if>]
                    <#break >
                <#default>
                    <#if !isEvent>parameters['${var_name}']<#else>${var_name}</#if> = clientMessage.read${util.capitalizeFirstLetter(util.getTsType(varType))}();
            </#switch>
            <#break >
        <#case "CUSTOM">
            <#if !isEvent>parameters['${var_name}']<#else>${var_name}</#if> = ${util.getTypeCodec(varType)?split(".")?last}.decode(clientMessage, toObjectFunction);
            <#break >
        <#case "COLLECTION">
        <#case "ARRAY">
            <#if cat == "COLLECTION">
            <#local itemVariableType= util.getGenericType(varType)>
            <#else>
            <#local itemVariableType= util.getArrayType(varType)>
            </#if>

            <#local itemVariableName= "${var_name}Item">
            <#local sizeVariableName= "${var_name}Size">
            <#local indexVariableName= "${var_name}Index">
        var ${sizeVariableName} = clientMessage.readInt32();
            <#if !isDefined>
            var ${var_name} : ${util.getTsType(varType)} = [];
            <#else>${var_name} = [];
            </#if>
        for(var ${indexVariableName} = 0 ;  ${indexVariableName} < ${sizeVariableName} ; ${indexVariableName}++){
        var ${itemVariableName} : ${util.getTsType(itemVariableType)};
            <@getterTextInternal var_name=itemVariableName varType=itemVariableType isEvent=true isCollection=true isDefined=true/>
        ${var_name}.push(${itemVariableName})
        }
            <#if !(isEvent || isCollection)>
            parameters['${var_name}'] = ${var_name};
            </#if>
            <#break >
        <#case "MAP">
            <#local sizeVariableName= "${var_name}Size">
            <#local indexVariableName= "${var_name}Index">
            <#local keyType = util.getFirstGenericParameterType(varType)>
            <#local valueType = util.getSecondGenericParameterType(varType)>
            <#local keyVariableName= "${var_name}Key">
            <#local valVariableName= "${var_name}Val">
        var ${sizeVariableName} = clientMessage.readInt32();
        var ${var_name} :any = {};
        for(var ${indexVariableName} = 0 ;  ${indexVariableName} < ${sizeVariableName} ; ${indexVariableName}++){
        var  ${keyVariableName} : any;
            <@getterTextInternal var_name=keyVariableName varType=keyType isEvent=true isDefined=false/>
            <@getterTextInternal var_name=valVariableName varType=valueType isEvent=true isDefined=false/>
        ${var_name}[${keyVariableName}] = ${valVariableName};
            <#if !isEvent>parameters['${var_name}'] = ${var_name};</#if>
        }
        <#break >
        <#case "MAPENTRY">
            <#local sizeVariableName= "${var_name}Size">
            <#local indexVariableName= "${var_name}Index">
            <#local keyType = util.getFirstGenericParameterType(varType)>
            <#local valueType = util.getSecondGenericParameterType(varType)>
            <#local keyVariableName= "${var_name}Key">
            <#local valVariableName= "${var_name}Val">
        var ${keyVariableName}: ${util.getTsType(keyType)};
        var ${valVariableName}: ${util.getTsType(valueType)};
            <@getterTextInternal var_name=keyVariableName isEvent=true varType=keyType />
            <@getterTextInternal var_name=valVariableName isEvent=true varType=valueType/>
        ${var_name} = [${keyVariableName}, ${valVariableName}];
    </#switch>
</#macro>