/*
* Copyright (c) 2014 Intel Corp. and others.  All rights reserved.
*
* This program and the accompanying materials are made available under the
* terms of the Eclipse Public License v1.0 which accompanies this distribution,
* and is available at http://www.eclipse.org/legal/epl-v10.html
*/
package org.opendaylight.sfc.provider.api;

import org.opendaylight.controller.sal.binding.api.BindingAwareBroker.ConsumerContext;

import com.google.common.base.Optional;
import org.opendaylight.controller.md.sal.binding.api.MountPoint;
import org.opendaylight.controller.md.sal.binding.api.MountPointService;
import org.opendaylight.sfc.provider.OpendaylightSfc;
import org.opendaylight.sfc.provider.SfcNetconfDataProvider;
import org.opendaylight.controller.sal.binding.api.RpcConsumerRegistry;
import org.opendaylight.yang.gen.v1.urn.intel.params.xml.ns.sf.desc.mon.rpt.rev141105.GetSFDescriptionOutput;
import org.opendaylight.yang.gen.v1.urn.intel.params.xml.ns.sf.desc.mon.rpt.rev141105.GetSFMonitoringInfoOutput;
import org.opendaylight.yang.gen.v1.urn.intel.params.xml.ns.sf.desc.mon.rpt.rev141105.ServiceFunctionDescriptionMonitorReportService;
import org.opendaylight.yangtools.yang.binding.InstanceIdentifier;
import org.opendaylight.yangtools.yang.common.RpcResult;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.concurrent.Future;
import com.google.common.base.Preconditions;
import static org.opendaylight.sfc.provider.SfcProviderDebug.printTraceStart;
import static org.opendaylight.sfc.provider.SfcProviderDebug.printTraceStop;

public class SfcProviderSfDescriptionMonitorAPI{
    private static final Logger LOG = LoggerFactory.getLogger(SfcProviderSfDescriptionMonitorAPI.class);
    private static final OpendaylightSfc odlSfc = OpendaylightSfc.getOpendaylightSfcObj();
    private static ConsumerContext sessionData;
    private static final InstanceIdentifier<?> NETCONF_NODES_PATH = null;

    public SfcProviderSfDescriptionMonitorAPI() {
            setSession();
    }

    protected void setSession()  {
        printTraceStart(LOG);
        try {
            if(sessionData==null) {
                sessionData = odlSfc.getBroker().registerConsumer(SfcNetconfDataProvider.GetNetconfDataProvider());
                Preconditions.checkState(sessionData != null,"SfcNetconfDataProvider register is not available.");
            }
        } catch (Exception e) {
            LOG.warn("failed to ...." , e);
        }
        printTraceStop(LOG);
    }

    public GetSFDescriptionOutput getSFDescriptionInfoFromNetconf(String mountpoint)  {
        printTraceStart(LOG);
        try {
            Future<RpcResult<GetSFDescriptionOutput>> result = getSfDescriptionMonitorService(mountpoint).getSFDescription();
            return result.get().getResult();
        } catch (Exception e) {
            LOG.warn("failed to ...." , e);
        }
        printTraceStop(LOG);
        return null;
    }

    public GetSFMonitoringInfoOutput getSFMonitorInfoFromNetconf(String mountpoint)  {
        printTraceStart(LOG);
        try {
            Future<RpcResult<GetSFMonitoringInfoOutput>> result = getSfDescriptionMonitorService(mountpoint).getSFMonitoringInfo();
            return result.get().getResult();
        } catch (Exception e) {
            LOG.warn("failed to ...." , e);
        }
        printTraceStop(LOG);
        return null;
    }

    private ServiceFunctionDescriptionMonitorReportService getSfDescriptionMonitorService(String mountpoint) {
        final InstanceIdentifier<?> path = NETCONF_NODES_PATH;
        MountPointService mountService = SfcNetconfDataProvider.GetNetconfDataProvider().getMountService();
        Preconditions.checkState(mountService != null, "Mount service is null");
        Optional<MountPoint> mountPoint = mountService.getMountPoint(path);
        Preconditions.checkState(mountPoint.isPresent(), "Mount point {} does not exists",mountPoint);
        final Optional<RpcConsumerRegistry> service = mountPoint.get().getService(RpcConsumerRegistry.class);
        Preconditions.checkState(service.isPresent());
        return service.get().getRpcService(ServiceFunctionDescriptionMonitorReportService.class);
    }

}
