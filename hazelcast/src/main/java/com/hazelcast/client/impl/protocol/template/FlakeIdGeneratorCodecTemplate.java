/*
 * Copyright (c) 2008-2017, Hazelcast, Inc. All Rights Reserved.
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

package com.hazelcast.client.impl.protocol.template;

import com.hazelcast.annotation.GenerateCodec;
import com.hazelcast.annotation.Request;
import com.hazelcast.annotation.Since;
import com.hazelcast.client.impl.protocol.constants.ResponseMessageConst;

@GenerateCodec(id = TemplateConstants.FLAKE_ID_GENERATOR_TEMPLATE_ID, name = "FlakeIdGenerator", ns = "Hazelcast.Client.Protocol.Codec")
public interface FlakeIdGeneratorCodecTemplate {

    @Request(id = 1, retryable = true, response = ResponseMessageConst.FLAKE_ID_ID_BATCH)
    @Since("1.6")
    Object newIdBatch(String name, int batchSize);
}
