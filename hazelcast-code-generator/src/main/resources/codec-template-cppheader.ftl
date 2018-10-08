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
#ifndef HAZELCAST_CLIENT_PROTOCOL_CODEC_${model.className?upper_case}_H_
#define HAZELCAST_CLIENT_PROTOCOL_CODEC_${model.className?upper_case}_H_

#if  defined(WIN32) || defined(_WIN32) || defined(WIN64) || defined(_WIN64)
#pragma warning(push)
#pragma warning(disable: 4251) //for dll export
#endif

#include <memory>
<#if typeExists("vector")>
#include <vector>
</#if>
<#if typeExists("string")>
#include <string>
</#if>
<#if typeExists("map")>
#include <map>
</#if>

#include "hazelcast/util/HazelcastDll.h"
#include "hazelcast/client/protocol/codec/${model.parentName}MessageType.h"
#include "hazelcast/client/protocol/ResponseMessageConst.h"
#include "hazelcast/client/impl/BaseEventHandler.h"
#include "hazelcast/client/protocol/ClientMessage.h"

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

using namespace hazelcast::client::serialization::pimpl;

namespace hazelcast {
    namespace client {
<#if shouldForwardDeclare("Data")>
        namespace serialization {
            namespace pimpl {
                class Data;
            }
        }
</#if>
<#if shouldForwardDeclare("Address")>
        class Address;
</#if>
<#if shouldForwardDeclare("Member")>
        class Member;
</#if>
<#if shouldForwardDeclare("MemberAttributeChange")>
        namespace impl {
            class MemberAttributeChange;
        }
</#if>
<#if shouldForwardDeclare("EntryView")>
        namespace map {
            class DataEntryView;
        }
</#if>
<#if shouldForwardDeclare("DistributedObjectInfo")>
        namespace impl {
                class DistributedObjectInfo;
        }
</#if>

        namespace protocol {
            namespace codec {
                class HAZELCAST_API ${model.className} {
                public:
                    static const ${model.parentName}MessageType REQUEST_TYPE;
                    static const bool RETRYABLE;
                    static const ResponseMessageConst RESPONSE_TYPE;
                    //************************ REQUEST STARTS ******************************************************************//
                        static std::auto_ptr<ClientMessage> encodeRequest(<#list model.requestParams as param>
                                <#if util.isPrimitive(param.type)>${util.getCppType(param.type)} ${param.name}<#else>const ${util.getCppType(param.type)} <#if param.nullable >*<#else>&</#if>${param.name}</#if><#if param_has_next>, </#if></#list>);

                        static int32_t calculateDataSize(<#list model.requestParams as param>
                                <#if util.isPrimitive(param.type)>${util.getCppType(param.type)} ${param.name}<#else>const ${util.getCppType(param.type)} <#if param.nullable >*<#else>&</#if>${param.name}</#if><#if param_has_next>, </#if></#list>);
                    //************************ REQUEST ENDS ********************************************************************//

                    <#if !isResponseVoid() >
                    //************************ RESPONSE STARTS *****************************************************************//
                    class HAZELCAST_API ResponseParameters {
                        public:
                            <#list model.responseParams as param>
                            <#if !param.nullable >${util.getCppType(param.type)} ${param.name};
                            <#else>std::auto_ptr<${util.getCppType(param.type)} > ${param.name};
                            </#if>
                            <#if param.sinceVersionInt gt model.messageSinceInt>bool ${param.name}Exist;</#if>
                            </#list>

                            static ResponseParameters decode(ClientMessage &clientMessage);

                            <#if responseHasNullable() >
                            // define copy constructor (needed for auto_ptr variables)
                            ResponseParameters(const ResponseParameters &rhs);
                            </#if>
                        private:
                            ResponseParameters(ClientMessage &clientMessage);
                    };
                    //************************ RESPONSE ENDS *******************************************************************//
                    </#if>

                    <#if model.events?has_content>

                    //************************ EVENTS START*********************************************************************//
                    class HAZELCAST_API AbstractEventHandler : public impl::BaseEventHandler {
                        public:
                            virtual ~AbstractEventHandler();

                            void handle(std::auto_ptr<protocol::ClientMessage> message);

                            <#list model.events as event>
                                <#assign paramCallList="">
                                <#assign previousVersion = event.sinceVersion?replace('.','') >
                                <#list event.eventParams as p>
                                    <#if p.versionChanged >
                                        virtual void handle${event.name?cap_first}EventV${previousVersion}(${paramCallList}) = 0;
                                        <#assign previousVersion = p.sinceVersion?replace('.','') >
                                    </#if>

                                    <#if p_index gt 0 ><#assign paramCallList=paramCallList + ", "></#if>
                                    <#if !p.nullable>
                                        <#assign paramCallList = paramCallList + "const " + util.getCppType(p.type) + " &" +  p.name>
                                    <#else>
                                        <#assign paramCallList = paramCallList + "std::auto_ptr<" + util.getCppType(p.type) + " > " +  p.name>
                                    </#if>
                                </#list>

                                    virtual void handle${event.name?cap_first}EventV${previousVersion}(${paramCallList}) = 0;

                            </#list>
                    };

                    //************************ EVENTS END **********************************************************************//
                    </#if>
                    private:
                        // Preventing public access to constructors
                        ${model.className} ();
                };
            }
        }
    }
}

#if  defined(WIN32) || defined(_WIN32) || defined(WIN64) || defined(_WIN64)
#pragma warning(pop)
#endif

#endif /* HAZELCAST_CLIENT_PROTOCOL_CODEC_${model.className?upper_case}_H_ */

<#--FUNCTIONS BELOW-->
<#function shouldIncludeHeader type>
    <#list model.responseParams as param>
        <#if param.type?contains(util.getCppType(type)) && false == param.nullable>
             <#return true>
        </#if>
    </#list>
    <#return false>
</#function>

<#function shouldForwardDeclare type>
    <#if shouldIncludeHeader(type) >
        <#return false>
    </#if>

    <#return typeExists(type)>
</#function>

<#function typeExists type>
    <#list model.requestParams as param>
        <#if util.getCppType(param.type)?contains(type)>
             <#return true>
        </#if>
    </#list>
    <#list model.responseParams as param>
        <#if util.getCppType(param.type)?contains(type)>
             <#return true>
        </#if>
    </#list>
<#if model.events?has_content>
    <#list model.events as event>
        <#list event.eventParams as param>
        <#if util.getCppType(param.type)?contains(type)>
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
