// Copyright (c) 2008-2019, Hazelcast, Inc. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package proto

<#global isImported = false>
import (
<#list model.requestParams as param><#if util.getGoType(param.type)?contains("Data") || util.getFirstGenericParameterType(param.type)?contains("Data") || util.getSecondGenericParameterType(param.type)?contains("Data")><#global isImported=true> "github.com/hazelcast/hazelcast-go-client/internal/serialization"<#break></#if></#list>
<#list model.events as event><#list event.eventParams as param><#if isImported><#break></#if><#if util.getGoType(param.type)?contains("Data") ><#global isImported=true> "github.com/hazelcast/hazelcast-go-client/internal/serialization"<#break></#if></#list></#list>
<#list model.responseParams as param><#if isImported><#break></#if><#if util.getGoType(param.type)?contains("Data") ><#global isImported=true> "github.com/hazelcast/hazelcast-go-client/internal/serialization"<#break></#if></#list>
<#list model.requestParams as param><#if util.getGoType(param.type) == "int32" || util.getGoType(param.type)?contains("[]") || util.getGoType(param.type) == "int64" || util.getGoType(param.type) == "bool" || util.getGoType(param.type) == "int64" ||util.getGoType(param.type) == "[]byte" || util.getGoType(param.type) == "[]int64">"github.com/hazelcast/hazelcast-go-client/internal/proto/bufutil"<#break></#if></#list>
)
<#--************************ REQUEST ********************************************************-->

func ${model.parentName?lower_case}${model.name?cap_first}CalculateSize(<#list model.requestParams as param>${param.name} ${util.getGoPointerType(param.type)}<#if param_has_next>, </#if></#list>) int {
    // Calculates the request payload size
    dataSize := 0
<#list model.requestParams as p>
    <@sizeText var_name=p.name type=p.type isNullable=p.nullable/>
</#list>
    return dataSize
}

// ${model.parentName}${model.name?cap_first}EncodeRequest creates and encodes a client message
// with the given parameters.
// It returns the encoded client message.
func ${model.parentName}${model.name?cap_first}EncodeRequest(<#list model.requestParams as param>${param.name} ${util.getGoPointerType(param.type)}<#if param_has_next>, </#if></#list>) *ClientMessage {
    // Encode request into clientMessage
    clientMessage := NewClientMessage(nil, ${model.parentName?lower_case}${model.name?cap_first}CalculateSize(<#list model.requestParams as param>${param.name}<#if param_has_next>, </#if></#list>))
    clientMessage.SetMessageType(${model.parentName?lower_case}${model.name?cap_first})
    clientMessage.IsRetryable =<#if model.retryable == 1>true<#else>false</#if>
<#list model.requestParams as p>
    <@setterText var_name=p.name type=p.type isNullable=p.nullable/>
</#list>
    clientMessage.UpdateFrameLength()
    return clientMessage
}

<#--************************ RESPONSE ********************************************************-->
<#if model.responseParams?has_content>
// ${model.parentName}${model.name?cap_first}DecodeResponse decodes the given client message.
// It returns a function which returns the response parameters.
func ${model.parentName}${model.name?cap_first}DecodeResponse(clientMessage *ClientMessage) func()(<#list model.responseParams as p>${p.name} ${util.getGoPointerType(p.type)}<#if p_has_next>, </#if></#list>) {
    // Decode response from client message
    return func()(<#list model.responseParams as p>${p.name} ${util.getGoPointerType(p.type)}<#if p_has_next>, </#if></#list>) {
    <#list model.responseParams as p>
        <#if p.versionChanged >
        if clientMessage.IsComplete() {
            return
        }
        </#if>
        <@getterText var_name=p.name type=p.type isNullable=p.nullable/>
    </#list>
        return
    }
}
<#else>// ${model.parentName}${model.name?cap_first}DecodeResponse(clientMessage *ClientMessage), this message has no parameters to decode
</#if>

<#--************************ EVENTS ********************************************************-->
<#if model.events?has_content>
<#--HANDLER FUNC TYPE DEF'S-->
    <#list model.events as event>
// ${model.parentName}${model.name?cap_first}HandleEvent${event.name?cap_first}Func is the event handler function.
type ${model.parentName}${model.name?cap_first}HandleEvent${event.name?cap_first}Func func(<#list event.eventParams as p>${util.getGoPointerType(p.type)}<#if p_has_next>, </#if></#list>)
    </#list>

<#--HANDLER DECODER FUNC'S-->
    <#list model.events as event>
// ${model.parentName}${model.name?cap_first}Event${event.name?cap_first}Decode decodes the corresponding event
// from the given client message.
// It returns the result parameters for the event.
func ${model.parentName}${model.name?cap_first}Event${event.name?cap_first}Decode(clientMessage *ClientMessage)(
        <#list event.eventParams as p>${p.name} ${util.getGoPointerType(p.type)}<#if p_has_next>, </#if></#list>) {
        <#list event.eventParams as p>
            <#if p.versionChanged >
    if clientMessage.IsComplete() {
        return
    }
            </#if>
            <@getterText var_name=p.name type=p.type isNullable=p.nullable/>
        </#list>
    return
}
    </#list>

// ${model.parentName}${model.name?cap_first}Handle handles the event with the given
// event handler function.
func ${model.parentName}${model.name?cap_first}Handle(clientMessage *ClientMessage,
    <#list model.events as event>handleEvent${event.name?cap_first} ${model.parentName}${model.name?cap_first}HandleEvent${event.name?cap_first}Func<#if event_has_next>,
    </#if></#list>){
    // Event handler
    messageType := clientMessage.MessageType()
    <#list model.events as event>
    if messageType == bufutil.Event${event.name?cap_first} && handleEvent${event.name?cap_first} != nil {
        handleEvent${event.name?cap_first}(${model.parentName}${model.name?cap_first}Event${event.name?cap_first}Decode(clientMessage))
    }
    </#list>
}
</#if>

<#--MACROS BELOW-->
<#--SIZE NULL CHECK MACRO -->
<#macro sizeText var_name type isNullable=false>
    <#if isNullable>
    dataSize += bufutil.BoolSizeInBytes
    if ${var_name} != <#if type?contains("String") || type?contains("string")>""<#else>nil</#if> {
        <@sizeTextInternal var_name=var_name type=type isNullable=true/>
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
<#macro sizeTextInternal var_name type isNullable=false pointer=true>
    <#local cat= util.getTypeCategory(type)>
    <#switch cat>
        <#case "OTHER">
            <#if util.isPrimitive(type)>
                dataSize += bufutil.${util.getGoType(type)?cap_first}SizeInBytes
            <#else >
                dataSize += ${util.getGoType(type)?lower_case}CalculateSize(${var_name})
            </#if>
            <#break >
        <#case "CUSTOM">
            dataSize += ${util.getGoType(type)?lower_case}CalculateSize(${var_name})
            <#break >
        <#case "COLLECTION">
            dataSize += bufutil.Int32SizeInBytes
            <#local genericType= util.getGenericType(type)>
            <#local n= var_name>
            for _,${var_name}Item := range ${var_name}{
            <@sizeTextInternal var_name="${n}Item"  type=genericType pointer=false/>
        }
            <#break >
        <#case "ARRAY">
            dataSize += bufutil.Int32SizeInBytes
            <#local genericType= util.getArrayType(type)>
            <#local n= var_name>
            for range ${var_name}{
            <@sizeTextInternal var_name="${n}Item"  type=genericType/>
        }
            <#break >
        <#case "MAPENTRY">
            <#local keyType = util.getFirstGenericParameterType(type)>
            <#local valueType = util.getSecondGenericParameterType(type)>
        key := ${var_name}.key.(${util.getGoPointerType(keyType)})
        val := ${var_name}.value.(${util.getGoPointerType(valueType)})
            <@sizeTextInternal var_name="key"  type=keyType />
            <@sizeTextInternal var_name="val"  type=valueType />
    </#switch>
</#macro>


<#--SETTER NULL CHECK MACRO -->
<#macro setterText var_name type isNullable=false>
    <#local isNullVariableName= "${var_name}IsNil">
    <#if isNullable>
    clientMessage.AppendBool(${var_name} == <#if type?contains("String") || type?contains("string")>""<#else>nil</#if>)
    if ${var_name} != <#if type?contains("String") || type?contains("string")>""<#else>nil</#if> {
        <@setterTextInternal var_name=var_name type=type isNullable=isNullable/>
    }
    <#else>
        <@setterTextInternal var_name=var_name type=type />
    </#if>
</#macro>

<#--SETTER MACRO -->
<#macro setterTextInternal var_name type isNullable=false pointer=true>
    <#local cat= util.getTypeCategory(type)>
    <#if cat == "OTHER">
        clientMessage.Append${util.getGoType(type)?cap_first}(${var_name})
    </#if>
    <#if cat == "CUSTOM">
        <#if type?contains("UUID")>UuidCodec<#else>${util.getTypeCodec(type)?split(".")?last}</#if>Encode(clientMessage, ${var_name})
    </#if>
    <#if cat == "COLLECTION">
        clientMessage.AppendInt32(int32(len(${var_name})))
        <#local itemType = util.getGenericType(type)>
        <#local itemTypeVar= var_name + "Item">
        for _,${itemTypeVar} := range ${var_name}{
        <@setterTextInternal var_name=itemTypeVar type=itemType pointer=false />
        }
    </#if>
    <#if cat == "ARRAY">
        clientMessage.AppendInt32(int32(len(${var_name})))
        <#local itemType= util.getArrayType(type)>
        <#local itemTypeVar= var_name + "Item">
        for _,${itemTypeVar} := range ${var_name}{
        <@setterTextInternal var_name=itemTypeVar  type=itemType />
        }
    </#if>
    <#if cat == "MAPENTRY">
        <#local keyType = util.getFirstGenericParameterType(type)>
        <#local valueType = util.getSecondGenericParameterType(type)>
                key := ${var_name}.key.(${util.getGoPointerType(keyType)})
                val := ${var_name}.value.(${util.getGoPointerType(valueType)})
        <@setterTextInternal var_name="key"  type=keyType />
        <@setterTextInternal var_name="val"  type=valueType />
    </#if>
</#macro>

<#--GETTER NULL CHECK MACRO -->
<#macro getterText var_name type isNullable=false isEvent=false >
    <#if isNullable><#if (isEvent)>var ${var_name} <#if !util.isPrimitive(type)>*</#if>${util.modifyForGoTypes(type?split(".")?last)}</#if>
        if !clientMessage.ReadBool(){
        <@getterTextInternal var_name=var_name varType=type isEvent=isEvent isNullable=isNullable/>
        }
    <#else>
        <@getterTextInternal var_name=var_name varType=type isEvent=isEvent/>
    </#if>
</#macro>

<#macro getterTextInternal var_name varType isEvent=false isCollection=false isNullable=false>
    <#local cat= util.getTypeCategory(varType)>
    <#local isDeserial= !(isEvent || isCollection)>
    <#switch cat>
        <#case "OTHER">
            <#switch varType>
                <#case util.DATA_FULL_NAME>
                    <#if !(isEvent || isCollection)>${var_name}<#else>${var_name} <#if isNullable==false>:</#if></#if>= clientMessage.ReadData()
                    <#break >
                <#case "java.lang.Integer">
                    <#if !(isEvent || isCollection)>${var_name}<#else>${var_name} <#if isNullable==false>:</#if></#if>= clientMessage.ReadInt32()
                    <#break >
                <#case "java.lang.Boolean">
                    <#if !(isEvent || isCollection)>${var_name}<#else>${var_name} <#if isNullable==false>:</#if></#if>= clientMessage.ReadBool()
                    <#break >
                <#case "java.lang.String">
                    <#if !(isEvent || isCollection)>${var_name}<#else>${var_name} <#if isNullable==false>:</#if></#if>= clientMessage.ReadString()
                    <#break >
                <#case "java.util.Map.Entry<com.hazelcast.nio.serialization.Data,com.hazelcast.nio.serialization.Data>">
                    <#if !(isEvent || isCollection)>${var_name}<#else>${var_name} <#if isNullable==false>:</#if></#if>= Pair{clientMessage.ReadData(), clientMessage.ReadData()}
                    <#break >
                <#default>
                    <#if !(isEvent || isCollection)>${var_name}<#else>${var_name} <#if isNullable==false>:</#if></#if>= clientMessage.Read${util.getGoType(varType)?cap_first}()
            </#switch>
            <#break >
        <#case "CUSTOM">
            <#if !(isEvent || isCollection)>${var_name}<#else>${var_name} <#if isNullable==false>:</#if></#if>= <#if varType?contains("UUID")>UuidCodec<#else>${util.getTypeCodec(varType)?split(".")?last}</#if>Decode(clientMessage)
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
            ${sizeVariableName} := clientMessage.ReadInt32()
            ${var_name} = make([]${util.getGoPointerType(itemVariableType)}, ${sizeVariableName})
            for ${indexVariableName} := 0 ; ${indexVariableName} < int(${sizeVariableName}) ; ${indexVariableName} ++ {
            <@getterTextInternal var_name=itemVariableName varType=itemVariableType isNullable= isNullable isEvent=isEvent isCollection=true/>
                ${var_name}[${indexVariableName}] = ${itemVariableName}
            }
            <#break >
        <#case "MAPENTRY">
            <#local sizeVariableName= "${var_name}Size">
            <#local indexVariableName= "${var_name}Index">
            <#local keyType = util.getFirstGenericParameterType(varType)>
            <#local valueType = util.getSecondGenericParameterType(varType)>
            <#local keyVariableName= "${var_name}Key">
            <#local valVariableName= "${var_name}Value">
            <@getterTextInternal var_name=keyVariableName varType=keyType isEvent=true/>
            <@getterTextInternal var_name=valVariableName varType=valueType isEvent=true/>
            var ${var_name} = &Pair{ key:${keyVariableName}, value:${valVariableName}}
    </#switch>
</#macro>
