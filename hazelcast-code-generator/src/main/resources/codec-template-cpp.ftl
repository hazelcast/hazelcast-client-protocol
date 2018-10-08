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

#include "hazelcast/util/Util.h"
#include "hazelcast/util/ILogger.h"

#include "hazelcast/client/protocol/codec/${model.className}.h"
<#if shouldIncludeHeader("Data")>
#include "hazelcast/client/serialization/pimpl/Data.h"
</#if>
<#if shouldIncludeHeader("Address")>
#include "hazelcast/client/Address.h"
</#if>
<#if shouldIncludeHeader("Member")>
#include "hazelcast/client/Member.h"
</#if>
<#if shouldIncludeHeader("MemberAttributeChange")>
#include "hazelcast/client/impl/MemberAttributeChange.h"
</#if>
<#if shouldIncludeHeader("EntryView")>
#include "hazelcast/client/map/DataEntryView.h"
</#if>
<#if shouldIncludeHeader("DistributedObjectInfo")>
#include "hazelcast/client/impl/DistributedObjectInfo.h"
</#if>
<#if shouldIncludeHeader("UUID")>
#include "hazelcast/util/UUID.h"
</#if>
<#if model.events?has_content>
#include "hazelcast/client/protocol/EventMessageConst.h"
</#if>

namespace hazelcast {
    namespace client {
        namespace protocol {
            namespace codec {
                const ${model.parentName}MessageType ${model.className}::REQUEST_TYPE = HZ_${model.parentName?upper_case}_${model.name?upper_case};
                const bool ${model.className}::RETRYABLE = <#if model.retryable == 1>true<#else>false</#if>;
                const ResponseMessageConst ${model.className}::RESPONSE_TYPE = (ResponseMessageConst) ${model.response};

                std::auto_ptr<ClientMessage> ${model.className}::encodeRequest(<#list model.requestParams as param>
                        <#if util.isPrimitive(param.type)>${util.getCppType(param.type)} ${param.name}<#else>const ${util.getCppType(param.type)} <#if param.nullable >*<#else>&</#if>${param.name}</#if><#if param_has_next>, </#if></#list>) {
                    int32_t requiredDataSize = calculateDataSize(<#list model.requestParams as param>${param.name}<#if param_has_next>, </#if></#list>);
                    std::auto_ptr<ClientMessage> clientMessage = ClientMessage::createForEncode(requiredDataSize);
                    clientMessage->setMessageType((uint16_t)${model.className}::REQUEST_TYPE);
                    clientMessage->setRetryable(RETRYABLE);
                    <#list model.requestParams as p>
                        <@setterText var_name=p.name type=p.type isNullable=p.nullable/>
                    </#list>
                    clientMessage->updateFrameLength();
                    return clientMessage;
                }

                int32_t ${model.className}::calculateDataSize(<#list model.requestParams as param>
                        <#if util.isPrimitive(param.type)>${util.getCppType(param.type)} ${param.name}<#else>const ${util.getCppType(param.type)} <#if param.nullable >*<#else>&</#if>${param.name}</#if><#if param_has_next>, </#if></#list>) {
                    int32_t dataSize = ClientMessage::HEADER_SIZE;
                    <#list model.requestParams as p>
                        <@sizeText var_name=p.name type=p.type isNullable=p.nullable/>
                    </#list>
                    return dataSize;
                }

                <#if !isResponseVoid() >
                    ${model.className}::ResponseParameters::ResponseParameters(ClientMessage &clientMessage) {
                        <#list model.responseParams as p><#if p.sinceVersionInt gt model.messageSinceInt >${p.name}Exist = false;</#if></#list>
                        <#list model.responseParams as p><#if p.versionChanged >if (clientMessage.isComplete()) {
                                    return;
                                }</#if>
                            <@getterText var_name=p.name type=p.type isNullable=p.nullable/>
                            <#if p.sinceVersionInt gt model.messageSinceInt >${p.name}Exist = true;</#if></#list>
                    }

                    ${model.className}::ResponseParameters ${model.className}::ResponseParameters::decode(ClientMessage &clientMessage) {
                        return ${model.className}::ResponseParameters(clientMessage);
                    }

                     <#if responseHasNullable() >
                    ${model.className}::ResponseParameters::ResponseParameters(const ${model.className}::ResponseParameters &rhs) {
                        <#list model.responseParams as param>
                        <#if param.nullable >
                            ${param.name} = std::auto_ptr<${util.getCppType(param.type)} >(new ${util.getCppType(param.type)}(*rhs.${param.name}));
                        <#else>
                            ${param.name} = rhs.${param.name};
                        </#if>
                        </#list>
                    }
                    </#if>
                </#if>

                <#if model.events?has_content>

                //************************ EVENTS START*************************************************************************//
                ${model.className}::AbstractEventHandler::~AbstractEventHandler() {
                }

                void ${model.className}::AbstractEventHandler::handle(std::auto_ptr<protocol::ClientMessage> clientMessage) {
                    int messageType = clientMessage->getMessageType();
                    switch (messageType) {
                    <#list model.events as event>
                        case protocol::EVENT_${event.name?upper_case}:
                        {
                            <#assign paramCallList="">
                            <#assign previousVersion = event.sinceVersion?replace('.','') >
                            <#list event.eventParams as p>
                                <#if p.versionChanged >
                                    if (clientMessage->isComplete()) {
                                        handle${event.name?cap_first}EventV${previousVersion}(${paramCallList});
                                        return;
                                    }
                                    <#assign previousVersion = p.sinceVersion?replace('.','') >
                                </#if>
                                <#if p_index gt 0 ><#assign paramCallList=paramCallList + ", "></#if>
                                <#assign paramCallList += p.name>
                                <@eventGetterText var_name=p.name type=p.type isNullable=p.nullable isEvent=true/>
                            </#list>

                                handle${event.name?cap_first}EventV${previousVersion}(${paramCallList});
                                break;
                        }
                        </#list>
                        default:
                            getLogger()->warning() << "[${model.className}::AbstractEventHandler::handle] Unknown message type (" << messageType << ") received on event handler.";
                    }
                }
                //************************ EVENTS END **************************************************************************//
                </#if>
            }
        }
    }
}

<#--MACROS BELOW-->
<#--SIZE NULL CHECK MACRO -->
<#macro sizeText var_name type isNullable=false>
<#local cat= util.getTypeCategory(type)>
<#switch cat>
            <#case "OTHER">
            <#case "CUSTOM">
                    dataSize += ClientMessage::calculateDataSize(${var_name});
                <#break >
            <#case "COLLECTION">
            <#local itemVariableType= util.getGenericType(type)>
                    dataSize += ClientMessage::calculateDataSize<${util.getCppType(itemVariableType)} >(${var_name});
                <#break >
            <#case "ARRAY">
                <#local itemVariableType= util.getArrayType(type)>
                    dataSize += ClientMessage::calculateDataSize<${util.getCppType(itemVariableType)} >(${var_name});
                <#break >
            <#case "MAP">
                <#local keyType = util.getFirstGenericParameterType(type)>
                <#local valueType = util.getSecondGenericParameterType(type)>
                    dataSize += ClientMessage::calculateDataSize<${util.getCppType(keyType)}, ${util.getCppType(valueType)} > (${var_name});
</#switch>
</#macro>

<#--SETTER NULL CHECK MACRO -->
<#macro setterText var_name type isNullable=false>
<#local cat= util.getTypeCategory(type)>
<#switch cat>
                <#case "OTHER">
                <#case "CUSTOM">
                    clientMessage->set(${var_name});
                    <#break >
                <#case "COLLECTION">
                <#local itemVariableType= util.getGenericType(type)>
                    clientMessage->setArray<${util.getCppType(itemVariableType)} >(${var_name});
                    <#break >
                <#case "ARRAY">
                <#local itemVariableType= util.getArrayType(type)>
                    clientMessage->setArray<${util.getCppType(itemVariableType)} > (${var_name});
                    <#break >
                <#case "MAP">
                    <#local keyType = util.getFirstGenericParameterType(type)>
                    <#local valueType = util.getSecondGenericParameterType(type)>
                    clientMessage->setEntryArray<${util.getCppType(keyType)}, ${util.getCppType(valueType)} >(${var_name});
                    <#break >
</#switch>
</#macro>

<#--GETTER NULL CHECK MACRO -->
<#macro getterText var_name type isNullable=false isEvent=false>
<#if isNullable>
    <#assign nullableStr = "Nullable">
<#else>
    <#assign nullableStr = "">
</#if>

<#local cat= util.getTypeCategory(type)>
<#switch cat>
                <#case "OTHER">
                <#case "CUSTOM">
                    ${var_name} = clientMessage.get${nullableStr}<${util.getCppType(type)} >();
                    <#break >
                <#case "COLLECTION">
                <#local itemVariableType= util.getGenericType(type)>
                    ${var_name} = clientMessage.get${nullableStr}Array<${util.getCppType(itemVariableType)} >();
                    <#break >
                <#case "ARRAY">
                <#local itemVariableType= util.getArrayType(type)>
                    ${var_name} = clientMessage.get${nullableStr}Array<${util.getCppType(itemVariableType)} >();
                    <#break >
                <#case "MAP">
                    <#local keyType = util.getFirstGenericParameterType(type)>
                    <#local valueType = util.getSecondGenericParameterType(type)>
                    ${var_name} = clientMessage.get${nullableStr}EntryArray<${util.getCppType(keyType)}, ${util.getCppType(valueType)} >();
                    <#break >
</#switch>
</#macro>

<#--Event getter MACRO -->
<#macro eventGetterText var_name type isNullable=false isEvent=false>
<#if isNullable>
    <#assign nullableStr = "Nullable">
<#else>
    <#assign nullableStr = "">
</#if>
<#local cat= util.getTypeCategory(type)>
<#switch cat>
                        <#case "OTHER">
                        <#case "CUSTOM">
                            <#if !isNullable >${util.getCppType(type)} ${var_name} = clientMessage->get${nullableStr}<${util.getCppType(type)} >();
                            <#else>std::auto_ptr<${util.getCppType(type)} > ${var_name} = clientMessage->get${nullableStr}<${util.getCppType(type)} >();
                            </#if>
                            <#break >
                        <#case "COLLECTION">
                        <#local itemVariableType= util.getGenericType(type)>
                            <#if !isNullable >${util.getCppType(type)} ${var_name} = clientMessage->get${nullableStr}Array<${util.getCppType(itemVariableType)} >();
                            <#else>std::auto_ptr<${util.getCppType(type)} > ${var_name} = clientMessage->get${nullableStr}Array<${util.getCppType(itemVariableType)} >();
                            </#if>
                            <#break >
                        <#case "ARRAY">
                        <#local itemVariableType= util.getArrayType(type)>
                            <#if !isNullable >${util.getCppType(type)} ${var_name} = clientMessage->get${nullableStr}Array<${util.getCppType(itemVariableType)} >();
                            <#else>std::auto_ptr<${util.getCppType(type)} > ${var_name} = clientMessage->get${nullableStr}Array<${util.getCppType(itemVariableType)} >();
                            </#if>
                            <#break >
                        <#case "MAP">
                            <#local keyType = util.getFirstGenericParameterType(type)>
                            <#local valueType = util.getSecondGenericParameterType(type)>
                            <#if !isNullable >${util.getCppType(type)} ${var_name} = clientMessage->get${nullableStr}EntryArray<${util.getCppType(keyType)}, ${util.getCppType(valueType)} >();
                            <#else>std::auto_ptr<${util.getCppType(type)} > ${var_name} = clientMessage->get${nullableStr}EntryArray<${util.getCppType(keyType)}, ${util.getCppType(valueType)} >();
                            </#if>
                            <#break >
</#switch>

</#macro>

<#function isHeaderAlreadyIncluded type>
    <#list model.responseParams as param>
        <#if param.type?contains(util.getCppType(type)) && false == param.nullable>
             <#return true>
        </#if>
    </#list>
    <#return false>
</#function>

<#--FUNCTIONS BELOW-->
<#function shouldIncludeHeader type>
    <#if isHeaderAlreadyIncluded(type)>
        <#return false>
    </#if>

    <#list model.requestParams as param>
        <#if param.type?contains(util.getCppType(type))>
             <#return true>
        </#if>
    </#list>
    <#if !isResponseVoid() >
        <#list model.responseParams as param>
            <#if param.type?contains(util.getCppType(type))>
                 <#return true>
            </#if>
        </#list>
    </#if>
<#if model.events?has_content>
    <#list model.events as event>
        <#list event.eventParams as param>
            <#if param.type?contains(util.getCppType(type))>
                 <#return true>
            </#if>
        </#list>
    </#list>
</#if>

<#return false>
</#function>

<#function responseHasNullable >
    <#list model.responseParams as param>
        <#if param.nullable>
             <#return true>
        </#if>
    </#list>

<#return false>
</#function>


<#function isResponseVoid >
    <#if model.response == 100 >
        <#return true>
    </#if>

    <#return false>
</#function>
