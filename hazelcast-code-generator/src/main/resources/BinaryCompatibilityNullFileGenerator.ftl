/*
 * Copyright (c) 2008-2019, Hazelcast, Inc. All Rights Reserved.
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

<#assign testForVersionString=util.versionAsString(testForVersion)/>
<#include "compatibility-common.ftl">
package com.hazelcast.client.protocol.compatibility;

import com.hazelcast.client.impl.MemberImpl;
import com.hazelcast.client.impl.client.DistributedObjectInfo;
import com.hazelcast.client.impl.protocol.ClientMessage;
import com.hazelcast.client.impl.protocol.codec.*;
import com.hazelcast.cluster.Member;
import com.hazelcast.internal.serialization.impl.HeapData;
import com.hazelcast.map.impl.SimpleEntryView;
import com.hazelcast.map.impl.querycache.event.DefaultQueryCacheEventData;
import com.hazelcast.map.impl.querycache.event.QueryCacheEventData;
import com.hazelcast.nio.Address;
import com.hazelcast.scheduledexecutor.ScheduledTaskHandler;
import com.hazelcast.nio.serialization.Data;
import com.hazelcast.transaction.impl.xa.SerializableXID;

import java.io.DataOutputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.lang.reflect.Array;
import java.net.UnknownHostException;
import javax.transaction.xa.Xid;
import java.util.AbstractMap;
import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.ListIterator;
import java.util.Map;

import static org.junit.Assert.assertTrue;
import static com.hazelcast.client.protocol.compatibility.ReferenceObjects.*;


public class BinaryCompatibilityNullFileGenerator {
    public static void main(String[] args) throws IOException {
        OutputStream out = new FileOutputStream("${testForVersionString}.protocol.compatibility.null.binary");
        DataOutputStream outputStream = new DataOutputStream(out);
<#list model?keys as key>
<#assign map=model?values[key_index]?values/>
<#if map?has_content>
<#list map as cm>

{
    ClientMessage clientMessage = ${cm.className}.encodeRequest( <#if cm.requestParams?has_content> <#list cm.requestParams as param> <#if param.nullable>null<#else>${convertTypeToSampleValue(param.type)}</#if> <#if param_has_next>, </#if> </#list> </#if>);
     outputStream.writeInt(clientMessage.getFrameLength());
     outputStream.write(clientMessage.buffer().byteArray(), 0 , clientMessage.getFrameLength());
}
{
    ClientMessage clientMessage = ${cm.className}.encodeResponse( <#if cm.responseParams?has_content> <#list cm.responseParams as param> <#if param.nullable>null<#else>${convertTypeToSampleValue(param.type)}</#if> <#if param_has_next>, </#if> </#list> </#if>);
    outputStream.writeInt(clientMessage.getFrameLength());
    outputStream.write(clientMessage.buffer().byteArray(), 0 , clientMessage.getFrameLength());
}
    <#if cm.events?has_content>
{
    <#list cm.events as event >
    {
        ClientMessage clientMessage = ${cm.className}.encode${event.name}Event(<#if event.eventParams?has_content> <#list event.eventParams as param> <#if param.nullable>null<#else>${convertTypeToSampleValue(param.type)}</#if> <#if param_has_next>, </#if> </#list> </#if>);
        outputStream.writeInt(clientMessage.getFrameLength());
        outputStream.write(clientMessage.buffer().byteArray(), 0 , clientMessage.getFrameLength());
     }
    </#list>
}
    </#if>

</#list>
</#if>
</#list>
         outputStream.close();
         out.close();

    }
}


<#--METHOD PARAM MACRO -->
<#macro methodParam type><#local cat= util.getTypeCategory(type)>
<#switch cat>
<#case "COLLECTION"><#local genericType= util.getGenericType(type)>java.util.Collection<${genericType}><#break>
<#default>${type}
</#switch>
</#macro>
